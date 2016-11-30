from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode("Taylor Swift")
print (location.latitude, location.longitude)