from pymongo import MongoClient #pip install pymongo
import json

with open('conf.json', 'r') as f:
    try:
        conf = json.load(f)
    except ValueError:
        conf = {}

ip_mongo = conf["ip_mongo"]

MONGODB_SERVER = ip_mongo
MONGODB_PORT = 27017
MONGODB_DB = "Grupo03"
P_E_COLLECTION = "preguntas_entidades_taller4"
P_E_UNWIND_COLLECTION = "preguntas_entidades_unwind_taller4"

connection = MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
p_e_collection = db[P_E_COLLECTION]
p_e_unwind_collection = db[P_E_UNWIND_COLLECTION]

resultado = p_e_collection.aggregate([{"$unwind":"$entities"}])
for i in resultado:
	del i["_id"]
	p_e_unwind_collection.insert(i)
