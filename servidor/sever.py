
from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS, cross_origin
import csv
from pymongo import MongoClient #pip install pymongo
from bson.json_util import dumps
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

connection = MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
p_e_collection = db[P_E_COLLECTION]


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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(host= '0.0.0.0', port=8080)