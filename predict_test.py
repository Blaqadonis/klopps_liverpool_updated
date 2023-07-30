import sys
import json
import requests


match = {
    "Previous match": sys.argv[1],  #"0",
    "Date":  sys.argv[2] ,  #"28-05-2023",
    "Form": sys.argv[3]  ,#"top",
    "Opposition": sys.argv[4] ,  #"poor",
    "season": sys.argv[5] , #"late",
    "venue": sys.argv[6]  ,#"away",
    "uEFa": sys.argv[7]  #"inactive"
}

URL = 'http://localhost:9696/predict'

response = requests.post(URL, json=match)

# Check the status code of the response
print("Status Code:", response.status_code)

try:
    # Try to decode the JSON response
    result = response.json()
    print(result)
except json.JSONDecodeError as e:
    print("JSONDecodeError:", e)
    print("Response Text:", response.text)
