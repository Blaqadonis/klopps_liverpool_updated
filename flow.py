import sys
import pickle
import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.tree import DecisionTreeClassifier
import mlflow
import prefect
from prefect import flow, task


mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("Klopps-Liverpool-experiment")

@task(retries=3, retry_delay_seconds=2, name="Read the csv file")
def read_dataframe(filepath: str):
    '''Reads the csv file and returns a dataframe'''
    data = pd.read_csv(filepath)

    data = data.applymap(lambda s: s.lower().replace(' ', '_') if isinstance(s, str) else s)
    data.columns = [x.lower().replace(' ', '_') for x in data.columns]
    data.columns = [x.lower().replace(':', '') for x in data.columns]
    data.columns = [x.lower().replace('*', '') for x in data.columns]
    data.columns = [x.lower().replace('.', '') for x in data.columns]

    data['date'] = pd.to_datetime(data['date'])
    return data

@task(retries=3, retry_delay_seconds=2, name="Preprocessing the data")
def preprocess(data: pd.DataFrame):
    '''Preprocesses the data'''
    data['day'] = data['date'].dt.day
    data['month'] = data['date'].dt.month
    data['year'] = data['date'].dt.year
    data = data.drop('date', axis=1)

    data['result'] = data['outcome'].replace(['win'], 1)
    data['result'] = data['result'].replace(['no_win'], 0)
    data['ground'] = data['venue'].replace(['home'], 1)
    data['ground'] = data['ground'].replace(['away'], 0)

    data['foreign_league'] = data['uefa'].replace(['active'], 1)
    data['foreign_league'] = data['foreign_league'].replace(['inactive'], 0)

    data['time'] = data['season'].replace(['early'], 0)
    data['time'] = data['time'].replace(['middle'], 1)
    data['time'] = data['time'].replace(['late'], 2)

    data['difficulty'] = data['opposition'].replace(['tough'], 2)
    data['difficulty'] = data['difficulty'].replace(['medium'], 1)
    data['difficulty'] = data['difficulty'].replace(['easy'], 0)

    data['current_form'] = data['form'].replace(['top'], 2)
    data['current_form'] = data['current_form'].replace(['decent'], 1)
    data['current_form'] = data['current_form'].replace(['poor'], 0)

    target = data['result']
    data = data.drop(['result', 'outcome', 'year', 'venue', 'uefa', 'season',
                       'opposition', 
                      'form'], 
                     axis=1)

    smote = SMOTE(random_state=42)
    data, target = smote.fit_resample(data, target)

    train_data, test_data, y_train_data, y_test = train_test_split(data, target, 
                                                                   test_size=0.2,
                                                                   random_state=30)
    train_data = train_data.reset_index(drop=True)
    test_data = test_data.reset_index(drop=True)
    y_train_data = y_train_data.reset_index(drop=True)
    y_test = y_test.reset_index(drop=True)

    majority = y_train_data.value_counts()[1]
    minority = y_train_data.value_counts()[0]

    big_smote = SMOTE(sampling_strategy={1: majority}, random_state=10)
    train_data1, y_train_data1 = big_smote.fit_resample(train_data, y_train_data)
    train_data2 = train_data1[y_train_data1 == 0][:minority]
    y_train_data2 = y_train_data1[y_train_data1 == 0][:minority]

    train_data = pd.DataFrame(np.concatenate((train_data2, train_data1[y_train_data1 == 1]),
                                              axis=0),
                              columns=train_data.columns)
    y_train_data = pd.DataFrame(np.concatenate((y_train_data2, y_train_data1[y_train_data1 == 1]),
                                                axis=0))

    return train_data, y_train_data, test_data, y_test

@task(retries=3, retry_delay_seconds=2, name="Search for best model")
def train_model_search(train_data, y_train_data, test_data, y_test):
    '''Trains the model using random search'''
    # Convert dataframes to numeric arrays
    vectorizer = DictVectorizer(sparse=False)
    X_train = vectorizer.fit_transform(train_data.to_dict(orient='records'))
    X_test = vectorizer.transform(test_data.to_dict(orient='records'))

    # Define the Decision Tree classifier
    tree = DecisionTreeClassifier()

    # Define the hyperparameter search space for random search
    param_distributions = {
        'criterion': ['gini', 'entropy'],
        'splitter': ['best', 'random'],
        'max_depth': [None, 10, 20, 30, 40, 50],  # You can extend the list as needed
    }

    # Perform random search with cross-validation
    random_search = RandomizedSearchCV(estimator=tree, param_distributions=param_distributions,
                                        cv=5)
    random_search.fit(X_train, y_train_data.values.ravel())

    # Get the best model from the random search
    best = random_search.best_estimator_

    # Fit the best model on the training data
    best.fit(X_train, y_train_data.values.ravel())

    # Make predictions on the training and test sets
    y_pred_train = best.predict(X_train)
    y_pred_test = best.predict(X_test)

    # Evaluate the model performance
    train_accuracy = accuracy_score(y_train_data, y_pred_train)
    test_accuracy = accuracy_score(y_test, y_pred_test)
    precision = precision_score(y_test, y_pred_test)
    recall = recall_score(y_test, y_pred_test)

    print('Best Model Parameters:', random_search.best_params_)
    print(f'Training-set accuracy score: {train_accuracy:0.4f}')
    print(f'Test-set accuracy score: {test_accuracy:0.4f}')
    print(f'Precision: {precision:0.2f}')
    print(f'Recall: {recall:0.2f}')

    return best, vectorizer

@task(retries=3, retry_delay_seconds=2, name="Log parameters and metrics to MLflow")
def mlflow_logging(model, train_data, y_train_data, test_data, y_test, name, vectorizer):
    '''Log the model parameters and metrics to MLflow'''
    # Start an MLflow run
    with mlflow.start_run():
        # Log the parameters and metrics to MLflow
        mlflow.log_params(model.get_params())
        mlflow.log_metric("train_accuracy", accuracy_score(y_train_data, model.predict(train_data)))
        mlflow.log_metric("test_accuracy", accuracy_score(y_test, model.predict(test_data)))
        mlflow.log_metric("precision", precision_score(y_test, model.predict(test_data)))
        mlflow.log_metric("recall", recall_score(y_test, model.predict(test_data)))      
        # Save the object
        with open('vectorizer.bin', 'wb') as file:
            pickle.dump(vectorizer, file)


        # Register the best model to MLflow model registry and log the vectorizer as an MLflow artifact
        mlflow.sklearn.log_model(model, name)
        mlflow.log_artifact("vectorizer.bin", "vectorizer")
   
@flow
def run():
    '''Run the flow'''
    model_name = sys.argv[2]
    file = read_dataframe(sys.argv[1])
    train_data, y_train_data, test_data, y_test = preprocess(file)
    best_model, vectorizer = train_model_search(train_data, y_train_data, test_data, y_test)
    mlflow_logging(best_model, train_data, y_train_data, test_data, y_test, model_name,vectorizer)

if __name__ == "__main__":
    run()
