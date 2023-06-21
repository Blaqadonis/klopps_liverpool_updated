import requests
import json

match = {
    "Previous match": "0",
    "Date": "28-05-2023",
    "Form": "top",
    "Opposition": "poor",
    "season": "late",
    "venue": "away",
    "uEFa": "inactive"
}

url = 'http://localhost:9696/predict'

response = requests.post(url, json=match)
result = response.json()
print(result)

