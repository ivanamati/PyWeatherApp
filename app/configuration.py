from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="geoapiExercises")
# Latitude & Longitude input

def dohvati_grad_iz_latitude_i_longitude(latitude,longitude):
    location = geolocator.reverse(f"{latitude},{longitude}")
    address = location.raw['address']
    grad = address.get('city')
    return grad

def Ivanec():
    latitude = "46.22306"
    longitude = "16.12"
    location = geolocator.reverse(f"{latitude},{longitude}")
    address = location.raw['address']
    grad = address.get('town')
    return grad

def Zagreb():
    dohvati_grad_iz_latitude_i_longitude(latitude = "45.82",longitude = "15.959999")

def Split():
    dohvati_grad_iz_latitude_i_longitude(latitude = "43.508133",longitude = "16.440193")


# GEOLOKATOR
# geolocator = Nominatim(user_agent="geoapiExercises")
# # Latitude & Longitude input
# Latitude = "45.82"
# Longitude = "15.959999"

# location = geolocator.reverse(f"{Latitude},{Longitude}")

# # Display
# #print(location)
# address = location.raw['address']
# #print(address)

# grad = address.get('city')
# drzava = address.get('country', '')
# print(f"{grad}, {drzava}")