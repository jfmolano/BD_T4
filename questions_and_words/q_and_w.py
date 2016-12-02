from pymongo import MongoClient
import json

with open('conf.json', 'r') as f:
    try:
        conf = json.load(f)
    except ValueError:
        conf = {}

ip_mongo = conf["ip_mongo"]

client = MongoClient(ip_mongo, 27017)
db = client['Grupo03']

collection_questions_w_entities = db['preguntas_entidades_taller4']
collection_questions_and_words = db['preguntas_palabras_taller4']

frequent = ["Alice_Cooper","Earth","United_States","Murph_(drummer)","Vito_Corleone","Santa_Claus","Amy_Winehouse","Paul_McCartney","English_language","Isle_of_Man"]

for f in frequent:
	question = collection_questions_w_entities.find({"entities.id":f})
	for q in question:
		collection_questions_and_words.insert({"word":f,"question":q["question"]})

