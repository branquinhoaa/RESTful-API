from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant, User
from findARestaurant import findARestaurant as find

from flask.ext.httpauth import HTTPBasicAuth
import json
import httplib2
from flask import make_response

auth = HTTPBasicAuth()

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__) 


# Here I can create my api routes with the specific action for each one

@app.route("/restaurants", methods=['GET', 'POST'])
@auth.login_required
def allRestaurants():
	if request.method == 'GET':
		return getAllRestaurants()
	if request.method == 'POST':
		location = request.json.get("location")
		mealtype = request.json.get("mealtype")
		print(request.args)
		return createARestaurant(location, mealtype)

@app.route("/restaurants/<int:id>", methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def restaurant(id):
	if request.method == 'GET':
		return getARestaurant(id)
	if request.method == 'PUT':
		name = request.json.get('name')
		address = request.json.get('address')
		image = request.json.get('image')
		return updateRestaurant(id, name, address, image)
	if request.method == 'DELETE':
		return deleteRestaurant(id)


# Generate methods to call - first endpoint
def getAllRestaurants():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])


def createARestaurant(location, mealtype):
	# Here I use my api findARestaurant to return the first restaurant
	# it will return name, address and image
	indication = find(mealtype, location)
	if type(indication) is not dict:
		return jsonify("no restaurant found")
	else:
		loc = ", ".join(indication["address"])

		# store the restaurant in the database
		restaurant = Restaurant(name = indication["name"], address=loc, image=indication["image"])
		session.add(restaurant)
		session.commit()

		# returns the restaurant for the user
		return jsonify(Restaurant=restaurant.serialize)

# Generate methods to call - second endpoint

def getARestaurant(id):
	restaurant = session.query(Restaurant).filter_by(id=id).one()
	if not restaurant:
		print("no restaurant")
	return jsonify(Restaurant=restaurant.serialize)

def updateRestaurant(id, name, address, image):
	restaurant = session.query(Restaurant).filter_by(id=id).one()
	if name:
		restaurant.name = name
	if address:
		restaurant.address = address
	if image:
		restaurant.image = image
	session.add(restaurant)
	session.commit()
	return jsonify(Restaurant=restaurant.serialize)

def deleteRestaurant(id):
	restaurant = session.query(Restaurant).filter_by(id=id).one()
	session.delete(restaurant)
	session.commit
	return "restaurant deleted"

# route to create my user

@app.route('/users', methods=['POST'])
def create_user():
	if request.method == 'POST':
		name = request.json.get('username')
		password = request.json.get('password')
		if name is None or password is None:
			abort(400)
		if session.query(User).filter_by(username=name).first():
			return("User is already created")
		user = User(username=name)
		user.hash_password(password)
		session.add(user)
		session.commit()
		return jsonify(User=user.username)

# authentication for my user

@auth.verify_password
def verify_password(username, password):
	user = session.query(User).filter_by(username= username).first()
	if not user or not user.verify_password(password):
		return False
	g.user = user
	return True



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)