#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants')
def restaurants():
    restaurants = Restaurant.query.all()
    restaurants_dict = [restaurant.to_dict() for restaurant in restaurants]

    response = make_response(
        jsonify(restaurants_dict),
        200
    )

    return response

@app.route('/restaurants/<string:id>')
def restaurantById(id):
    restaurant = Restaurant.query.filter_by(id=id).first()

    if restaurant:
        restaurant_dict = restaurant.to_dict()
        restaurant_dict['pizzas'] = [restaurant_pizza.pizza.to_dict() for restaurant_pizza in restaurant.restaurant_pizzas]

        response = make_response(
            jsonify(restaurant_dict),
            200
        )

    else:
        response = make_response(
            {"error": "Restaurant not found"},
            404
        )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
