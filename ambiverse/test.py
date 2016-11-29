import requests
import ast

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

token = ast.literal_eval(response.text)["access_token"]

