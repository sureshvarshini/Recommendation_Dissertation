from flask_restful import Resource
from flask import request, jsonify, make_response
from models.Model import Food, Rating, User
from recommendation.RecommendFood import get_food_recommendations, daily_calorie_intake, extract_macro_nutrients


class FoodRecommendationResource(Resource):
    def get(self, id):
        user = User.fetch_by_id(id=id)
        
        calories = daily_calorie_intake(user)
        print("----------------> CALORIES")
        print(calories)

        macro_nutrients_ratio = extract_macro_nutrients(calories=calories, user=user)
        print("-------------")
        print(macro_nutrients_ratio)

        similar_food_ids = get_food_recommendations(id)

        food_response = []

        for food_id in similar_food_ids:
            db_food = Food.fetch_by_id(id=food_id)

            food_object = {
                "id": db_food.id,
                "Name": db_food.name,
                "Calories": db_food.calories,
                "Cholesterol": db_food.cholesterol,
                "Folic Acid": db_food.folic_acid,
                "Vitamin C": db_food.vitamin_c,
                "Vitamin D": db_food.vitamin_d,
                "Calcium": db_food.calcium,
                "Iron": db_food.iron,
                "Protein": db_food.protein,
                "Carbohydrate": db_food.carbohydrate,
                "Fiber": db_food.fiber,
                "Sugars": db_food.sugars,
                "Fat": db_food.fat
            }

            food_response.append(food_object)

        return make_response(jsonify({
            "recommended_foods": food_response
        }), 201)


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
