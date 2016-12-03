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
BD_ENTIDADES_COLLECTION = "tw_y_bd_taller4"
E_TW_COLLECTION = "entidades_tw_taller4"
ACTORS_COLLECTION = "actores_taller4"

connection = MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
bd_entidades_collection = db[BD_ENTIDADES_COLLECTION]
e_tw_collection = db[E_TW_COLLECTION]
actors_collection = db[ACTORS_COLLECTION]

counter = 0
start_time = time.time()

resultado = e_tw_collection.find({},{"_id":False})
for i in resultado:
	id_ent = i["entities"]["id"]
	words = id_ent.split("_")
	and_list = []
	for word in words:
		and_list.append({"rn":{"$regex":".*"+word.replace("(","").replace(")","")+".*"}})
	actors = actors_collection.find({"$and":and_list})
	actors_list = list(actors)
	if len(actors_list)>0:
		actor = actors_list[0]
		db = actor["db"]
		dd = actor["dd"]
	else:
		db = None
		dd = None
	i["dd"] = dd
	i["db"] = db
	bd_entidades_collection.insert(i)
	counter = counter+1
	progreso = counter/2451.0
	t_act = time.time() - start_time
	t_res = (1.0/progreso - 1.0)*t_act
	print "Porcentaje: "+str(progreso*100.0)+" %"+" Restante: "+str(int(t_res/3600))+":"+str(int(t_res/60)%60)+":"+str(int(t_res)%60) + " Actual: "+str(int(t_act/3600))+":"+str(int(t_act/60)%60)+":"+str(int(t_act)%60)
