import httplib2
import json
import sys
import enviromental_variables as env


def getGeocodeLocation(nameOfThePlace):
	google_api_key=env.getGoogleApiKey()
	place_to_search = nameOfThePlace.replace(" ", "+")
	url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'%(place_to_search, google_api_key))
	
	http = httplib2.Http()
	response, content = http.request(url, 'GET')
	result = json.loads(content)
	lat = result['results'][0]['geometry']['location']['lat']
	longit = result['results'][0]['geometry']['location']['lng'] 
	return lat, longit


def findARestaurant(mealType, location):
	lat, longit = getGeocodeLocation(location)
	place = getAPlace(lat, longit, mealType)
	response = {}
	response["name"] = place["name"]
	response["address"] = place["location"]["formattedAddress"]
	
	try:
		response["image"] = place["categories"][0]["icon"]["prefix"] + place["categories"][0]["icon"]["suffix"]  
	except:
		response["image"] = "default.jpg" 
	
	return response



def getAPlace(lat, longit, mealType):
	fourSquare_id, fourSquare_secret=env.getForsquareIdAndSecret()
	url = ('https://api.foursquare.com/v2/venues/search?ll=%s,%s&query=%s&v=20180323&client_secret=%s&client_id=%s'%(lat, longit, mealType, fourSquare_secret, fourSquare_id))
	http = httplib2.Http()
	response, content = http.request(url, 'GET')
	result = json.loads(content)
	return result["response"]["venues"][0]
