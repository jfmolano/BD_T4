# -*- coding: utf-8 -*-

import requests
import ast
import json
from pymongo import MongoClient
from geopy.geocoders import Nominatim
import time
import re, string

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

## get token

def get_simple_entities(texto):
	url = "https://api.ambiverse.com/v1beta3/entitylinking/analyze"

	texto = texto.replace("\"","")

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

	##print response.text

	return ast.literal_eval(response.text)["matches"]

def get_entities(texto):
	url = "https://api.ambiverse.com/v1beta3/entitylinking/analyze"

	texto = texto.replace("\"","").replace("\n"," ").replace("(","").replace(")","").replace("\'"," ").replace("\t"," ").replace("\r"," ").replace("\\"," ").replace("]","").replace("[","").replace("/","").replace("—","")
	#texto = "Brad Pitt is gay"

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

	#print data

	response = requests.request("POST", url, data=data, headers=headers)

	#print response.text

	matches = ast.literal_eval(response.text)["matches"]

	##print matches

	entities = []

	for m in matches:
		#print m
		if "id" in m["entity"]:
			entidad_id = m["entity"]["id"]
			url = "https://api.ambiverse.com/v1beta3/knowledgegraph/entities?offset=0&limit=10"
			data = "[\""+entidad_id+"\"]"

			headers = {
			    'Content-Type': "application/json",
			    'Accept': "application/json",
			    'Authorization': token
			    }

			response = requests.request("POST", url, data=data, headers=headers)
			entities.append(ast.literal_eval(response.text)["entities"][0])

	return entities

def get_token():
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
	#print response.text
	return ast.literal_eval(response.text)["access_token"]

###
###
###

token = get_token()

with open('conf.json', 'r') as f:
    try:
        conf = json.load(f)
    except ValueError:
        conf = {}

ip_mongo = conf["ip_mongo"]

client = MongoClient(ip_mongo, 27017)
db = client['Grupo03']

collection_questions = db['preguntas_taller4']
collection_entities = db['entidades_taller4']
collection_questions_w_entities = db['preguntas_entidades_taller4']

questions = collection_questions.find({},{"_id":False}).skip(215)

counter = 0
start_time = time.time()

for question in questions:
	try:
		#print question

		question_description = question["description"]
		question_answer_1 = question["answer_1"]

		if question_answer_1 != None:
			text = question_description + " " + question_answer_1
		else:
			text = question_description
		#print text
		list_entities = get_entities(text)

		list_question_entities = []

		#print " "
		for i in list_entities:
			if "categories" in i:
				categories_set = set(i["categories"])
				#print i["id"]
				if "YAGO3:<yagoPermanentlyLocatedEntity>" in categories_set:
					id_entity = i["id"].replace("YAGO3:<","").replace(">","")
					text_geolocator = id_entity.replace("_"," ")
					geolocator = Nominatim()
					try:
						location = geolocator.geocode(text_geolocator)
						lon = location.longitude
						lat = location.latitude
					except:
						lon = 0
						lat = 0
					#Semantic enrichment
					enrichment_items = []
					if "description" in i:
						description = i["description"]
						list_description_entities = get_entities(description)
						#print list_description_entities
						enrichment_items = []
						for j in list_description_entities:
							if "categories" in j:
								id_entity_se = j["id"].replace("YAGO3:<","").replace(">","")

								#Object generation
								obj = {"type":2,"id":id_entity_se}
								enrichment_items.append(obj)

						#End of semantic enrichment

					#Object generation
					obj = {"type":1,"id":id_entity,"geometry":{"lat":lat,"lon":lon},"enrichment":enrichment_items}
					list_question_entities.append(obj)

				elif "YAGO3:<wordnet_person_100007846>" in categories_set:

					id_entity = i["id"].replace("YAGO3:<","").replace(">","")

					#Semantic enrichment
					enrichment_items = []
					if "description" in i:
						description = i["description"]
						list_description_entities = get_entities(description)
						#print list_description_entities
						enrichment_items = []
						for j in list_description_entities:
							if "categories" in j:
								categories_set = set(j["categories"])
								if "YAGO3:<yagoPermanentlyLocatedEntity>" in categories_set:
									id_entity_se = j["id"].replace("YAGO3:<","").replace(">","")
									text_geolocator = id_entity_se.replace("_"," ")
									geolocator = Nominatim()
									try:
										location = geolocator.geocode(text_geolocator)
										lon_entity = location.longitude
										lat_entity = location.latitude
									except:
										lon_entity = 0
										lat_entity = 0

									#Object generation
									obj = {"type":2,"id":id_entity_se,"geometry":{"lat":lat_entity,"lon":lon_entity}}
									enrichment_items.append(obj)

								else:
									id_entity_se = j["id"].replace("YAGO3:<","").replace(">","")

									#Object generation
									obj = {"type":2,"id":id_entity_se}
									enrichment_items.append(obj)

					#End of semantic enrichment

					#Object generation
					obj = {"type":1,"id":id_entity,"enrichment":enrichment_items}
					list_question_entities.append(obj)

				else:

					id_entity = i["id"].replace("YAGO3:<","").replace(">","")
					obj = {"type":3,"id":id_entity}
					list_question_entities.append(obj)

		for i in list_question_entities:
			#print i
			#print " "
			collection_entities.insert(i)

		question["entities"] = list_question_entities
		collection_questions_w_entities.insert(question)

		counter = counter+1
		progreso = counter/150.0
		t_act = time.time() - start_time
		t_res = (1.0/progreso - 1.0)*t_act
		print "Porcentaje: "+str(progreso*100.0)+" %"+" Restante: "+str(int(t_res/3600))+":"+str(int(t_res/60)%60)+":"+str(int(t_res)%60) + " Actual: "+str(int(t_act/3600))+":"+str(int(t_act/60)%60)+":"+str(int(t_act)%60)
	except:
		print "Error"

