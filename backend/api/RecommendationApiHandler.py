from flask_restful import Resource
from flask import request, jsonify, make_response
from datetime import datetime
from models.Model import Food, Rating, User, Water
from recommendation.RecommendFood import daily_calorie_intake, extract_macro_nutrients, choose_foods, get_similar_foods_recommendation, get_similar_users_recommendations, get_hybrid_recommendation
from caching import cache


class FoodRecommendationResource(Resource):
    # To cache every 24 hours in seconds, timeout = 86400
    @cache.cached(timeout=120)
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

        temp_id= []
        recommended_meal_choices = {}
        similar_meal_choices = {}
        for meal_type, meal_options in food_choices.items():
            recommended_response = []
            similar_food_response = []
            for food_id in meal_options:
                temp_id.append(food_id)
                db_food = Food.fetch_by_id(id=food_id)
                db_food_object = {
                    "id": db_food.id,
                    "Name": db_food.name,
                    "Servings": db_food.servings,
                    "Ingredients": db_food.ingredients,
                    "Directions": db_food.directions,
                    "Quantity": str(meal_options[food_id]) + 'g',
                    "Calories": db_food.calories,
                    "Image": db_food.image
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
                    "Servings": similar_food.servings,
                    "Ingredients": similar_food.ingredients,
                    "Directions": similar_food.directions,
                    "Calories": similar_food.calories,
                    "Image": similar_food.image
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
                "Servings": rated_food.servings,
                "Ingredients": rated_food.ingredients,
                "Directions": rated_food.directions,
                "Calories": rated_food.calories,
                "Image": rated_food.image
            }
            rated_food_choices.append(rated_food_object)

        hybrid_recommendation_ids = get_hybrid_recommendation(similar_users_recommendation_food_ids=rated_food_ids, foods=all_foods, chosen_food_id=temp_id)

        hybrid_food_choices = []
        for id in hybrid_recommendation_ids:
            food = Food.fetch_by_id(id=id)
            food_object = {
                "id": food.id,
                "Name": food.name,
                "Servings": food.servings,
                "Ingredients": food.ingredients,
                "Directions": food.directions,
                "Calories": food.calories,
                "Image": food.image
            }
            hybrid_food_choices.append(food_object)


        return make_response(jsonify({
            "recommended_foods": recommended_meal_choices,
            "similar_food_choices": similar_meal_choices,
            "similar_user_food_choices": rated_food_choices,
            "hybrid_food_choices": hybrid_food_choices
        }), 200)


class AddRatingResource(Resource):
    def post(self):

        data = request.get_json()

        user_id = data["user_id"]
        food_id = data["food_id"]
        rating = data["rating"]

        # Check if the user has previously rated the food, if yes update the row or add a new rating row
        old_rating = Rating.fetch_by_user_and_food_id(
            id=user_id, food_id=food_id)
        if old_rating is not None:
            print('Updating row')
            old_rating.rating = rating
            old_rating.save()
        else:
            print('Creating new row')
            new_rating = Rating(
                user_id=user_id, food_id=food_id, rating=rating)
            new_rating.save()

        return make_response(jsonify({
            "message": "Rating updated successfuly.",
            "status": 201
        }), 201)


class ViewRatingResource(Resource):
    def get(self, id, food_id):
        user_rating = Rating.fetch_by_user_and_food_id(id=id, food_id=food_id)

        if user_rating is not None:
            rating = user_rating.rating
        else:
            rating = 0

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
            water_quantity = Water(
                user_id=id, amount=data['amount'], last_entry=datetime.now())

        water_quantity.save()

        return make_response(jsonify({
            "message": "Water intake updated successfuly.",
            "status": 201
        }), 201)

    # Check water intake limit reached
    def get(self, id):
        water_quantity = Water.fetch_by_user_id(id=id)

        if water_quantity is None:
            return make_response(jsonify({
                "water_status_code": -1,
                "message": "You have not started logging your water intake.",
                "status": 200
            }), 200)

        # 1 cup ~ 250ml
        # 7 cups = 1700ml

        if water_quantity.amount >= 1700:  # ml
            return make_response(jsonify({
                "water_status_code": 1,
                "message": "Goal achieved! You've had enough water for the day.",
                "status": 200
            }), 200)
        else:
            cups = round((1700 - water_quantity.amount)/250)
            remaining_water = 1700 - water_quantity.amount
            return make_response(jsonify({
                "water_status_code": 0,
                "remaining_ml": remaining_water,
                "remaining_cups": cups,
                "message": f"Keep drinking! You still need {1700 - water_quantity.amount} liters.",
                "status": 200
            }), 200)
