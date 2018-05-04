from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant
from findARestaurant import findARestaurant as find


engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__) 


# Here I can create my api routes with the specific action for each one

@app.route("/restaurants", methods=['GET', 'POST'])
def allRestaurants():
	if request.method == 'GET':
		return getAllRestaurants()
	if request.method == 'POST':
		createARestaurant()

@app.route("/restaurant/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def restaurant():
	if request.method == 'GET':
		getARestaurant(id)
	if request.method == 'PUT':
		updateRestaurant(id)
	if request.method == 'DELETE':
		deleteRestaurant(id)


# Generate methods to call - first endpoint

def getAllRestaurants():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])


def createARestaurant(location, mealtype):
	# Here I use my api findARestaurant to return the first restaurant
	# it will return name, address and image
	indication = find(mealtype, location)

	# store the restaurant in the database
	restaurant = Restaurant(name = indication["name"], address=indication["address"], image=indication["image"])
	session.add(restaurant)
	session.commit()

	# returns the restaurant for the user
	return jsonify(Restaurant=restaurant.serialize)

# Generate methods to call - second endpoint

def getARestaurant(id):
	print("showing restaurant")

def updateRestaurant(id):
	print("updating restaurant")

def deleteRestaurant(id):
	print("deleting a restaurant")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)