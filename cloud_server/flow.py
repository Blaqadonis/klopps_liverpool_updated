import os
import pandas as pd
import pickle
from mlflow.tracking import MlflowClient
import mlflow
from flask import Flask, request, jsonify

MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
RUN_ID = 'fcbdb588ba56435bb3e561b74dc7310a'
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

with open('model/pipeline.bin', 'rb') as f_in:
    model = pickle.load(f_in)

def prepare_features(data):
    data = pd.DataFrame(data, index=range(0, 1))
    data.columns = [x.lower() for x in data.columns]
    data['date'] = pd.to_datetime(data['date'], dayfirst=True)
    data['day'] = data['date'].dt.day

    data = data.applymap(lambda s: s.lower().replace(' ', '_') if type(s) == str else s)
    data.columns = [x.lower().replace(' ', '_').replace(':', '').replace('*', '').replace('.', '') for x in data.columns]

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
    dicts = data.to_dict(orient='records')
    return dicts


def predict(dicts):
    X = dicts
    pred = model.predict(X)
    return float(pred[0])


app = Flask("Klopps_Liverpool")


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    match = request.get_json()
    dicts = prepare_features(match)
    pred = predict(dicts)

    if pred == 1:
        result = {
            "Prediction": "Safe to bet"
        }
    else:
        result = {
            "Prediction": "Unsafe to bet"
        }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
