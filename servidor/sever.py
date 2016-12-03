
from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS, cross_origin
import csv
from datetime import datetime
from pymongo import MongoClient #pip install pymongo
from bson.json_util import dumps
import json
from collections import Counter

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
P_E_U_COLLECTION = "preguntas_entidades_unwind_taller4"
E_TW_COLLECTION = "entidades_tw_taller4"
E_DB_TW_COLLECTION = "tw_y_bd_taller4"
WORDS_COLLECTION = "preguntas_palabras_taller4"

connection = MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
p_e_collection = db[P_E_COLLECTION]
p_e_u_collection = db[P_E_U_COLLECTION]
e_tw_collection = db[E_TW_COLLECTION]
e_db_tw_collection = db[E_DB_TW_COLLECTION]
words_collection = db[WORDS_COLLECTION]


app = Flask(__name__)
CORS(app)

marcas = [
    {
        'Id': u'1',
        'Dato': u'A'
    },
    {
        'Id': u'2',
        'Dato': u'B'
    }
]

@app.route('/api/marcas', methods=['GET'])
def get_marcas():
	return jsonify({'marcas': marcas})

@app.route('/api/dar_marca', methods=['POST'])
def dar_marca_post():
	if not request.json or not 'Id' in request.json:
		abort(400)
	marca = {
	'Id': request.json['Id'],
	'Dato': request.json.get('Dato', "")
	}
	return jsonify({'marca': marca}), 201

@app.route('/api/dar_marca/<Id>/<Dato>', methods=['GET'])
def dar_marca_get(Id,Dato):
	marca = {
	'Id': Id,
	'Dato': Dato
	}
	return jsonify({'marca': marca}), 201

@app.route('/info_preguntas', methods=['GET'])
def info_preguntas():
	print "Entra a servicio"
	resultado = p_e_collection.find({},{"_id":False})
	l = list(resultado)
	return dumps(l), 201

@app.route('/info_georef', methods=['GET'])
def info_georef():
	print "Entra a servicio"
	resultado = p_e_collection.aggregate([{"$unwind":"$entities"},{"$match":{"entities.geometry":{"$exists":True},"entities.enrichment":{"$exists":True}}}])
	l = list(resultado)
	return dumps(l), 201

@app.route('/info_entidad', methods=['GET'])
def info_entidad():
	print "Entra a servicio"
	resultado = p_e_u_collection.find({},{"_id":False})
	l = list(resultado)
	return dumps(l), 201

@app.route('/info_geo_people', methods=['GET'])
def info_geo_people():
	print "Entra a servicio"
	#Use no date collection
	resultado = p_e_u_collection.find({"entities.enrichment.geometry":{"$exists":True}},{"_id":False})
	l = list(resultado)
	return dumps(l), 201

@app.route('/info_tw_people', methods=['GET'])
def info_tw_people():
	print "Entra a servicio"
	resultado = e_tw_collection.find({},{"_id":False})
	l = list(resultado)
	return dumps(l), 201

@app.route('/info_tw_people_post', methods=['POST'])
def info_tw_people_post():
	if not request.json:
		abort(400)
	fini = request.json["fini"]
	ffin = request.json["ffin"]
	print fini
	print ffin
	obj_consulta = {}
	if fini != "-" and ffin == "-":
		obj_consulta["db"] = {"$gt":datetime.strptime(fini,'%d-%m-%Y')}
	elif fini == "-" and ffin != "-":
		obj_consulta["db"] = {"$lt":datetime.strptime(ffin,'%d-%m-%Y')}
	elif fini != "-" and ffin != "-":
		obj_consulta["db"] = {"$gt":datetime.strptime(fini,'%d-%m-%Y'),"$lt":datetime.strptime(ffin,'%d-%m-%Y')}
	print obj_consulta
	resultado = e_db_tw_collection.find(obj_consulta,{"_id":False})
	l = list(resultado)
	l_ret = []
	for i in l:
		if i["db"] != None:
			try:
				i["db"] = i["db"].strftime('%d-%m-%Y')
			except:
				i["db"] = None
		l_ret.append(i)
	return dumps(l_ret), 201

@app.route('/questions_words', methods=['GET'])
def questions_words():
	print "Entra a servicio"
	resultado = words_collection.find({},{"_id":False})
	return_object = {}
	for question in resultado:
		if not question["word"] in return_object:
			return_object[question["word"]] = [question["question"]]
		else:
			return_object[question["word"]].append(question["question"])
	return_list = []
	for key in return_object:
		if len(return_object[key])>1:
			return_list.append({"word":key,"questions":'   -   '.join(return_object[key])})
	return dumps(return_list), 201

@app.route('/tag_cloud', methods=['GET'])
def tag_cloud():
	obj = {}
	resultado = p_e_u_collection.find({},{"_id":False})
	for i in resultado:
		id_ent = i["entities"]["id"]
		movie = i["movie"]
		if not movie in obj:
			obj[movie] = [id_ent]
		else:
			obj[movie].append(id_ent)

	#print obj
	dictlist = []
	for key, value in obj.iteritems():
		cnt = Counter(value)
		l = []
		for k in cnt:
			l.append({"word":k,"count":cnt[k]})
		temp = {"movie":key,"word_list":l}
		dictlist.append(temp)
	return dumps(dictlist), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(host= '0.0.0.0', port=8080)