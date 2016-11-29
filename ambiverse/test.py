import requests
import ast
import json

## get token

url = "https://api.ambiverse.com/oauth/token"

with open('conf.json', 'r') as f:
    try:
        conf = json.load(f)
    except ValueError:
        conf = {}

client_id = conf["client_id"]
client_secret = conf["client_secret"]

data = "client_id="+client_id+"&client_secret="+client_secret+"&grant_type=client_credentials"

headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Accept': "application/json"
    }

response = requests.request("POST", url, data=data, headers=headers)
print response.text

token = ast.literal_eval(response.text)["access_token"]

## analyze - get entities

url = "https://api.ambiverse.com/v1beta3/entitylinking/analyze"

texto = "When Who played Tommy in Columbus, Pete was at his best."

data = "{"+ \
  "\"coherentDocument\": true,"+  \
  "\"confidenceThreshold\": 0.075,"+ \
  "\"docId\": \"doc1\","+ \
  "\"text\": \""+texto+"\","+ \
  "\"language\": \"en\""+ \
"}"

#print data

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Authorization': token
    }

response = requests.request("POST", url, data=data, headers=headers)

matches = ast.literal_eval(response.text)["matches"]

for m in matches:
	entidad_id = m["entity"]["id"]
	url = "https://api.ambiverse.com/v1beta3/knowledgegraph/entities?offset=0&limit=10"
	data = "[\""+entidad_id+"\"]"

	headers = {
	    'Content-Type': "application/json",
	    'Accept': "application/json",
	    'Authorization': token
	    }

	response = requests.request("POST", url, data=data, headers=headers)

	print response.text
