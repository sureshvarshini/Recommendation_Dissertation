from flask_restful import Resource
from flask import request, jsonify, make_response
from models.Model import Food, Rating, User
from recommendation.RecommendFood import get_food_recommendations, daily_calorie_intake, extract_macro_nutrients, choose_foods, get_similar_foods


class FoodRecommendationResource(Resource):
    def get(self, id):
        # id - user_id
        user = User.fetch_by_id(id=id)
        food_response = []

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
                recommended_response.append(db_food_object)

            # Fetch foods similar to 'food_id'
            similar_food_ids = get_similar_foods(
                food_id=food_id, foods=all_foods)
            for id in similar_food_ids:
                similar_food = Food.fetch_by_id(id=id)
                similar_food_object = {
                    "id": similar_food.id,
                    "Name": similar_food.name,
                    "Directions": similar_food.directions,
                    "Calories": similar_food.calories,
                    "Vitamin C": similar_food.vitamin_c,
                    "Vitamin D": similar_food.vitamin_d,
                    "Calcium": similar_food.calcium,
                    "Protein": similar_food.protein,
                    "Carbohydrate": similar_food.carbohydrates,
                    "Fiber": similar_food.fiber,
                    "Sugars": similar_food.sugars,
                    "Fat": similar_food.fat
                }
                similar_food_response.append(similar_food_object)

            recommended_meal_choices[meal_type] = recommended_response
            similar_meal_choices[meal_type] = similar_food_response

        # Fetch foods - highest rating by user
        ratings = Rating.fetch_all_ratings()
        rated_food_ids = get_food_recommendations(id, ratings)

        rated_food_choices = []
        for id in rated_food_ids:
            rated_food = Food.fetch_by_id(id=id)
            rated_food_object = {
                "id": rated_food.id,
                "Name": rated_food.name,
                "Directions": rated_food.directions,
                "Calories": rated_food.calories,
                "Vitamin C": rated_food.vitamin_c,
                "Vitamin D": rated_food.vitamin_d,
                "Calcium": rated_food.calcium,
                "Protein": rated_food.protein,
                "Carbohydrate": rated_food.carbohydrates,
                "Fiber": rated_food.fiber,
                "Sugars": rated_food.sugars,
                "Fat": rated_food.fat
            }
            rated_food_choices.append(rated_food_object)

        return make_response(jsonify({
            "recommended_foods": recommended_meal_choices,
            "similar_food_choices": similar_meal_choices,
            "rated_food_choices": rated_food_choices
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
