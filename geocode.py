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
	first_place = getAPlace(lat, longit, mealType)[0]
	venue_id = first_place["id"]
	response = {}
	response["name"] = first_place["name"]
	response["address"] = first_place["location"]["formattedAddress"]
	response["image"] = getFourSquarePhoto(venue_id)
	return response


def getAPlace(lat, longit, mealType):
	fourSquare_id, fourSquare_secret=env.getForsquareIdAndSecret()
	url = ('https://api.foursquare.com/v2/venues/search?ll=%s,%s&query=%s&v=20180323&client_secret=%s&client_id=%s'%(lat, longit, mealType, fourSquare_secret, fourSquare_id))
	http = httplib2.Http()
	response, content = http.request(url, 'GET')
	result = json.loads(content)
	return result["response"]["venues"]


def getFourSquarePhoto(venue_id):
	fourSquare_id, fourSquare_secret=env.getForsquareIdAndSecret()
	photo_size = '300x300'
	url = ('https://api.foursquare.com/v2/venues/%s/photos?client_secret=%s&client_id=%s&v=20180323'%(venue_id, fourSquare_secret, fourSquare_id))

	http = httplib2.Http()
	response, content = http.request(url, 'GET')

	# the content returns a list of pictures, but I just want the first one
	content = json.loads(content)
	first_pic = content["response"]["photos"]["items"][0]
	pic_url = first_pic["prefix"]+ photo_size + first_pic["suffix"]

	return pic_url