from flask_restful import Resource
from flask import request, jsonify, make_response
from models.Model import Food, Rating, User, Water
from recommendation.RecommendFood import daily_calorie_intake, extract_macro_nutrients, choose_foods, get_similar_foods_recommendation, get_similar_users_recommendations


class FoodRecommendationResource(Resource):
    def get(self, id):
        # id - user_id
        user = User.fetch_by_id(id=id)

        # Calculate the calorie intake and macro nutrients split to consume per day - customized to each person
        calories = daily_calorie_intake(user=user)
        macro_nutrients_ratio = extract_macro_nutrients(
            calories=calories, user=user)

        print("---------------------------")
        print("MACRO NUTRIENTS RATIO")
        print(macro_nutrients_ratio)

        # Pick out foods that fall under calculated calories and macro nutrients
        all_foods = Food.fetch_all_foods()
        food_choices = choose_foods(
            macro_nutrients_ratio=macro_nutrients_ratio, foods=all_foods)

        recommended_meal_choices = {}
        similar_meal_choices = {}
        for meal_type, meal_options in food_choices.items():
            recommended_response = []
            similar_food_response = []
            for food_id in meal_options:
                db_food = Food.fetch_by_id(id=food_id)
                db_food_object = {
                    "id": db_food.id,
                    "Name": db_food.name,
                    "Directions": db_food.directions,
                    "Quantity": str(meal_options[food_id]) + 'g',
                    "Calories": db_food.calories
                }
                recommended_response.append(db_food_object)

            # Fetch foods similar to 'food_id'
            similar_food_ids = get_similar_foods_recommendation(
                food_id=food_id, foods=all_foods)
            for food_id in similar_food_ids:
                similar_food = Food.fetch_by_id(id=food_id)
                similar_food_object = {
                    "id": similar_food.id,
                    "Name": similar_food.name,
                    "Directions": similar_food.directions,
                    "Calories": similar_food.calories
                }
                similar_food_response.append(similar_food_object)

            recommended_meal_choices[meal_type] = recommended_response
            similar_meal_choices[meal_type] = similar_food_response

        # Fetch foods - highest rating by similar users
        ratings = Rating.fetch_all_ratings()
        users = User.fetch_all_users()
        rated_food_ids = get_similar_users_recommendations(id, ratings, users)

        rated_food_choices = []
        for id in rated_food_ids:
            rated_food = Food.fetch_by_id(id=id)
            rated_food_object = {
                "id": rated_food.id,
                "Name": rated_food.name,
                "Directions": rated_food.directions,
                "Calories": rated_food.calories
            }
            rated_food_choices.append(rated_food_object)

        return make_response(jsonify({
            "recommended_foods": recommended_meal_choices,
            "similar_food_choices": similar_meal_choices,
            "similar_user_food_choices": rated_food_choices
        }), 200)


class AddRatingResource(Resource):
    def post(self):

        data = request.get_json()

        user_id = data["user_id"]
        food_id = data["food_id"]
        rating = data["rating"]

        new_rating = Rating(user_id=user_id, food_id=food_id, rating=rating)

        new_rating.save()

        return make_response(jsonify({
            "message": "Rating updated successfuly.",
            "status": 201
        }), 201)


class ViewRatingResource(Resource):
    def get(self, id):
        all_ratings = Rating.fetch_by_user_id(id=id)
        rating = []
        food_id = []

        for db_rating in all_ratings:
            food_id.append(db_rating.food_id)
            rating.append(db_rating.rating)

        return make_response(jsonify({
            "user_id": id,
            "food_id": food_id,
            "rating": rating
        }), 200)


class ActivityRecommendationResource(Resource):
    def get(self, id):
        return "Hello there!"


class WaterRecommendationResource(Resource):
    # Log water intake
    def post(self, id):
        data = request.get_json()
        amount = data['amount']
        water_quantity = Water.fetch_by_user_id(id=id)

        if water_quantity is not None:
            if amount:
                water_quantity.amount = amount + water_quantity.amount
        else:
            water_quantity = Water(user_id=id, amount=data['amount'])
        
        water_quantity.save()

        return make_response(jsonify({
            "message": "Water intake updated successfuly.",
            "status": 201
        }), 201)

    # Check water intake limit reached
    def get(self, id):
        water_quantity = Water.fetch_by_user_id(id=id)
        print("WATER --------")
        print(water_quantity)

        if water_quantity is None:
            return make_response(jsonify({
                "water_status_code": -1,
                "message": "You have not started logging your water intake.",
                "status": 200
            }), 200)

        if water_quantity.amount >= 1500:  # ml
            return make_response(jsonify({
                "water_status_code": 1,
                "message": "Goal achieved! You've had enough water for the day.",
                "status": 200
            }), 200)
        else:
            return make_response(jsonify({
                "water_status_code": 0,
                "message": f"Keep drinking! You still need {1500 - water_quantity.amount} liters.",
                "status": 200
            }), 200)
