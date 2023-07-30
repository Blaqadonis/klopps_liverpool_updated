import pickle
#import numpy as np
from flask import Flask, request, jsonify
import pandas as pd

# Load the pre-trained model and vectorizer using pickle
with open('pipeline.bin', 'rb') as f_in:
    model = pickle.load(f_in)


app = Flask("Klopps_Liverpool")

def prepare_features(data):
    '''Preprocess the input data and make predictions using the pre-trained model'''
    # Create a DataFrame with a single row containing the input data
    data = pd.DataFrame(data, index=[0])

    # Preprocess the input data (similar to the preprocessing during training)
    data = data.applymap(lambda s: s.lower().replace(' ', '_') if isinstance(s, str) else s)
    data.columns = [x.lower().replace(' ', '_').replace(':', '').replace('*', '').replace('.', '')
                    for x in data.columns]
    data['date'] = pd.to_datetime(data['date'], dayfirst=True)
    data['day'] = data['date'].dt.day
    
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

    data = data.drop(['venue', 'uefa', 'season', 'opposition', 'form', 'date'], axis=1)

    return data

def predict(data):
    '''Preprocess the input data and make predictions using the pre-trained model'''
    dicts = data.to_dict(orient='records')

    # Use the vectorizer to transform the data to the same format as during training
    #data_transformed = dv.transform(data)

    # Make predictions using the pre-trained model
    pred = model.predict(dicts)

    return pred


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    '''Endpoint for making predictions'''
    try:
        data = request.get_json()
        dicts = prepare_features(data)
        pred = predict(dicts)

        if pred[0] == 1:
            result = {"Prediction": "Safe to bet"}
        else:
            result = {"Prediction": "Unsafe to bet"}

        return jsonify(result)

    except Exception as error:
        return jsonify({"Error": str(error)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
