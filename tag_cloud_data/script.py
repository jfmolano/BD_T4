from pymongo import MongoClient #pip install pymongo
from collections import Counter
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
TG_COLLECTION = "tg_taller4"

connection = MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
entidades_collection = db[ENTIDADES_COLLECTION]
tg_collection = db[TG_COLLECTION]

counter = 0
start_time = time.time()

obj = {}

resultado = entidades_collection.find({},{"_id":False})
for i in resultado:
	id_ent = i["entities"]["id"]
	movie = i["movie"]
	if not movie in obj:
		obj[movie] = [id_ent]
	else:
		obj[movie].append(id_ent)
	counter = counter+1
	progreso = counter/2451.0
	t_act = time.time() - start_time
	t_res = (1.0/progreso - 1.0)*t_act
	print "Porcentaje: "+str(progreso*100.0)+" %"+" Restante: "+str(int(t_res/3600))+":"+str(int(t_res/60)%60)+":"+str(int(t_res)%60) + " Actual: "+str(int(t_act/3600))+":"+str(int(t_act/60)%60)+":"+str(int(t_act)%60)

#print obj
dictlist = []
for key, value in obj.iteritems():
	cnt = Counter(value)
	l = []
	for k in cnt:
		l.append({"word":k,"count":cnt[k]})
	temp = {"movie":key,"word_list":l}
	dictlist.append(temp)
print dictlist


