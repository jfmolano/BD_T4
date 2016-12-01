from dateutil.parser import parse
from pymongo import MongoClient

with open('conf.json', 'r') as f:
    try:
        conf = json.load(f)
    except ValueError:
        conf = {}

ip_mongo = conf["ip_mongo"]

client = MongoClient(ip_mongo, 27017)
db = client['Grupo03']
collection_actores = db['actores_taller4']

#with open("/home/pi/biographies.list") as f:
with open("out.list") as f:
    rn = None
    db = None
    dd = None
    for line in f:
	if line.startswith( '------' ):
		try:
			if rn != None and db != None:
				if dd != None:
					dd = parse(dd)
				collection_actores.insert({"rn":rn,"db":parse(db),"dd":dd})
		except:
			print "Date format error"
		rn = None
		db = None
		dd = None
	if line.startswith( 'RN:' ):
		rn = line.replace("RN: ","").replace("\n","")
	if line.startswith( 'DB:' ):
		db = line.replace("DB: ","").replace("\n","").split(",")[0]
	if line.startswith( 'DD:' ):
		dd = line.replace("DD: ","").replace("\n","").split(",")[0]
