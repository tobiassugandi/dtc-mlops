import json
import base64
import boto3

kinesis_client = boto3.client('kinesis')
PREDICTIONS_STREAM_NAME = 'ride_predictions'

def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

def predict(features):#, model=model):
    return 10.0
    # preds = model.predict(features)
    # return preds[0]

def lambda_handler(event, context):
    # Print event to debug
    # print("Received event: ", json.dumps(event, indent=2))

    # Check if the event has 'Records' key
    if 'Records' not in event:
        print("Warning: 'Records' key not found in event")
        return {
            'statusCode': 400,
            'body': json.dumps("Invalid event format: Missing 'Records' key")
        }

    # Process each record
    for record in event['Records']:
        if 'kinesis' in record and 'data' in record['kinesis']:
            encoded_data = record['kinesis']['data']
            decoded_data = base64.b64decode(encoded_data).decode('utf-8')
            print("Decoded Data: ", decoded_data)

            ride_event = json.loads(decoded_data)
            ride = ride_event["ride"]
            ride_id = ride_event["ride_id"]

            features = prepare_features(ride)
            preds = predict(features)

            # Send prediction to Kinesis
            prediction_event = {
                'model': 'ride_duration_prediction_model',
                'version': '123',
                'prediction': {
                    'ride_duration': preds,
                    'ride_id': ride_id,
                }
            }

            kinesis_client.put_record(
                StreamName=PREDICTIONS_STREAM_NAME,
                Data=json.dumps(prediction_event),
                PartitionKey=str(ride_id)#the identifier of the record
            )

            print("Prediction sent to Kinesis: ", prediction_event)

        else:
            print("Warning: 'kinesis' or 'data' key missing in record", record)

    return {
        'statusCode': 200,
        'body': json.dumps("Processing complete")
    }
