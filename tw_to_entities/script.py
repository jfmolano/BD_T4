from pymongo import MongoClient #pip install pymongo
import json
import time

with open('conf.json', 'r') as f:
    try:
        conf = json.load(f)
    except ValueError:
        conf = {}

ip_mongo = conf["ip_mongo"]

MONGODB_SERVER = ip_mongo
MONGODB_PORT = 27017
MONGODB_DB = "Grupo03"
ENTIDADES_COLLECTION = "preguntas_entidades_unwind_taller4"
E_TW_COLLECTION = "entidades_tw_taller4"
TWEETS_COLLECTION = "tweets_taller4"

connection = MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
entidades_collection = db[ENTIDADES_COLLECTION]
e_tw_collection = db[E_TW_COLLECTION]
tweets_collection = db[TWEETS_COLLECTION]

counter = 0
start_time = time.time()

resultado = entidades_collection.find({},{"_id":False})
for i in resultado:
	id_ent = i["entities"]["id"]
	words = id_ent.split("_")
	and_list = []
	for word in words:
		and_list.append({"text":{"$regex":".*"+word.replace("(","").replace(")","")+".*"}})
	tweets = tweets_collection.find({"$and":and_list}).limit(8)
	tw_list = []
	for tweet in tweets:
		tw_list.append({"text":tweet["text"],"user":tweet["user"]["screen_name"],"date":tweet["created_at"]})
	if len(tw_list) > 0:
		i["tweets"] = tw_list
		e_tw_collection.insert(i)
	counter = counter+1
	progreso = counter/2451.0
	t_act = time.time() - start_time
	t_res = (1.0/progreso - 1.0)*t_act
	print "Porcentaje: "+str(progreso*100.0)+" %"+" Restante: "+str(int(t_res/3600))+":"+str(int(t_res/60)%60)+":"+str(int(t_res)%60) + " Actual: "+str(int(t_act/3600))+":"+str(int(t_act/60)%60)+":"+str(int(t_act)%60)
