import requests

ride_info = {
    "PULocationID": 10,
    "DOLocationID": 50,
    "trip_distance": 35
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=ride_info)
print(f"{response.status_code=}")  # Print HTTP status code
print(f"{response.json()= }")  # Print the actual response content
