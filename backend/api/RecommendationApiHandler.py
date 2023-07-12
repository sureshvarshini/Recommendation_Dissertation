from flask_restful import Resource
from flask import request, jsonify, make_response
from models.Model import Food

class FoodRecommendationResource(Resource):
    def get(self, id):
        db_food = Food.fetch_by_id(id=id)

        if db_food is not None:
            return make_response(jsonify({
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

            }), 200)

        return make_response(jsonify({
            "message": f"Food '{id}' does not exist.",
            "status": 404
        }), 404)
