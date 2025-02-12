import pickle
from flask import Flask, request, jsonify
import mlflow

mlflow.set_tracking_uri("http://host.docker.internal:5050")
model_name = 'pipelined-lin-reg'
model_version_alias = "first"

model_uri = f"models:/{model_name}@{model_version_alias}"
model = mlflow.sklearn.load_model(model_uri)

def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

def predict(features, model=model):
    preds = model.predict(features)
    return preds[0]

### Create wrapper for flask ###
app = Flask('duration-prediction')
            
@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    # ML prediction
    features = prepare_features(ride)
    preds = predict(features)

    result = {
        'duration': preds
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)


