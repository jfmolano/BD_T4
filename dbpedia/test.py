from SPARQLWrapper import SPARQLWrapper, JSON

query = "PREFIX dbres: <http://dbpedia.org/resource/>" + "\n" + 
"DESCRIBE dbres:United_States"

print query

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

sparql.setQuery(query)  # the previous query as a literal string

print sparql.query().convert()
