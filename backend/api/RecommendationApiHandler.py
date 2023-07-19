from flask_restful import Resource
from flask import request, jsonify, make_response
from models.Model import Food, Rating, User
from recommendation.RecommendFood import get_food_recommendations, daily_calorie_intake, extract_macro_nutrients, choose_foods, get_collaborative_recommendations


class FoodRecommendationResource(Resource):
    def get(self, id):
        user = User.fetch_by_id(id=id)
        food_response = []

        # Calculate the calorie intake and macro nutrients split to consume per day - customized to each person
        calories = daily_calorie_intake(user)
        macro_nutrients_ratio = extract_macro_nutrients(
            calories=calories, user=user)
        
        print("---------------------------")
        print("MACRO NUTRIENTS RATIO")
        print(macro_nutrients_ratio)

        # Pick out foods that fall under calculated calories and macro nutrients
        foods = Food.fetch_all_foods()
        food_choices = choose_foods(
            macro_nutrients_ratio=macro_nutrients_ratio, foods=foods)

        recommended_meal_choices = {}
        for meal_type, meal_options in food_choices.items():
            response = []
            for food_id in meal_options:
                db_food = Food.fetch_by_id(id=food_id)
                db_food_object = {
                    "id": db_food.id,
                    "Name": db_food.name,
                    "Directions": db_food.directions,
                    "Quantity": str(meal_options[food_id]) +'g',
                    "Calories": db_food.calories,
                    "Vitamin C": db_food.vitamin_c,
                    "Vitamin D": db_food.vitamin_d,
                    "Calcium": db_food.calcium,
                    "Protein": db_food.protein,
                    "Carbohydrate": db_food.carbohydrates,
                    "Fiber": db_food.fiber,
                    "Sugars": db_food.sugars,
                    "Fat": db_food.fat
                }
                response.append(db_food_object)
            recommended_meal_choices[meal_type] = response

        # Return food recommendations - hybrid recoommendation
        ratings = Rating.fetch_all_ratings()
        similar_food_ids = get_food_recommendations(id, ratings)

        for food_id in similar_food_ids:
            db_food = Food.fetch_by_id(id=food_id)

            food_object = {
                "id": db_food.id,
                "Name": db_food.name,
                "Calories": db_food.calories,
                "Vitamin C": db_food.vitamin_c,
                "Vitamin D": db_food.vitamin_d,
                "Calcium": db_food.calcium,
                "Protein": db_food.protein,
                "Carbohydrate": db_food.carbohydrates,
                "Fiber": db_food.fiber,
                "Sugars": db_food.sugars,
                "Fat": db_food.fat
            }

            food_response.append(food_object)

        return make_response(jsonify({
            "recommended_foods": recommended_meal_choices
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
