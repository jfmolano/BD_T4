with open("/home/pi/biographies.list") as f:
    rn = None
    db = None
    dd = None
    for line in f:
	if line.startswith( '------' ):
		if rn != None and db != None and dd != None:
			print {"rn":rn,"db":db,"dd":dd}
		rn = None
		db = None
		dd = None
	if line.startswith( 'RN:' ):
		rn = line.replace("RN: ","")
	if line.startswith( 'DB:' ):
		db = line.replace("DB: ","")
	if line.startswith( 'DD:' ):
		dd = line.replace("DD: ","")
