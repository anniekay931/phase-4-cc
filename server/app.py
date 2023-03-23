#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.orm import sessionmaker

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

@app.route('/restaurants/<int:id>')
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

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)

    if restaurant:
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()
        db.session.delete(restaurant)
        db.session.commit()

        response = make_response('', 204)

    else:
        response = make_response(
            {"error": "Restaurant not found"},
            404
        )

    return response

@app.route('/pizzas')
def pizzas():
    pizzas = Pizza.query.all()
    pizzas_dict = [pizza.to_dict() for pizza in pizzas]

    response = make_response(
        jsonify(pizzas_dict),
        200
    )

    return response

@app.route('/restaurant_pizzas', methods=['POST'])
def restaurant_pizzas():
    try:
        price = int(request.form['price'])
        if price < 1 or price > 30:
            raise ValueError

        pizza_id = int(request.form['pizza_id'])
        restaurant_id = int(request.form['restaurant_id'])

        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)

        if not pizza or not restaurant:
            raise ValueError

        new_restaurant_pizza = RestaurantPizza(
            price=price,
            pizza_id=pizza_id,
            restaurant_id=restaurant_id
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()

        restaurant_pizza_dict = new_restaurant_pizza.to_dict()

        response = make_response(
            jsonify(restaurant_pizza_dict),
            201
        )

    except (ValueError, KeyError):
        response = make_response(
            {"error": "Invalid input"},
            400
        )

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
