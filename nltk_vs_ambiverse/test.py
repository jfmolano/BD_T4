import spacy
nlp = spacy.load('en')
doc = nlp(u'Union Station is an Amtrak railroad station and commercial building in downtown Erie in the U.S. state of Pennsylvania. It is the only stop in Pennsylvania for the Lake Shore Limited, a passenger rail line serving Chicago, New York City, and Boston.')
print doc.ents
for ent in doc.ents:
    print(ent.label_, ent.text)