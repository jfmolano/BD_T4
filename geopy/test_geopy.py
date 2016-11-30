from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode("Bogota")
print (location.latitude, location.longitude)