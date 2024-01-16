from geopy.geocoders import Nominatim  
geo_locator = Nominatim(user_agent = "Estates.Solutions")  
place_1 = "RidgePoint Irving, Texas, USA"
location = geo_locator.geocode(place_1)  
print(location)     