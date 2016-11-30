# -*- coding: utf-8 -*-

import requests
import ast
import json
from geopy.geocoders import Nominatim

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

	##print data

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

	texto = texto.replace("\"","")

	data = "{"+ \
	  "\"coherentDocument\": true,"+  \
	  "\"confidenceThreshold\": 0.075,"+ \
	  "\"docId\": \"doc1\","+ \
	  "\"text\": \""+texto+"\","+ \
	  "\"language\": \"en\""+ \
	"}"

	##print data

	headers = {
	    'Content-Type': "application/json",
	    'Accept': "application/json",
	    'Authorization': token
	    }

	response = requests.request("POST", url, data=data, headers=headers)

	##print response.text

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

	return ast.literal_eval(response.text)["access_token"]

###
###
###

token = get_token()

question = "Brad Pitt visited Angelina Jolie and they traveled to Africa."

list_entities = get_entities(question)

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
			obj = {"id":id_entity,"geometry":{"lat":lat,"lon":lon}}
			list_question_entities.append(obj)

		elif "YAGO3:<wordnet_person_100007846>" in categories_set:

			id_entity = i["id"].replace("YAGO3:<","").replace(">","")

			#Semantic enrichment

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

for i in list_question_entities:
	print i
	print " "


