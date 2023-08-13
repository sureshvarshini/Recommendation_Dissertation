import pandas as pd

from flask_restful import Resource
from flask import request, jsonify, make_response
from datetime import datetime
from models.Model import Food, Rating, User, Water, Activity, ADL
from recommendation.RecommendFood import daily_calorie_intake, extract_macro_nutrients, choose_foods, get_similar_foods_recommendation, get_similar_users_recommendations, get_hybrid_recommendation
from recommendation.ActivityLevel import analyse_free_times
from caching import cache

# List of foods to avoid based on illness
FOODS_AVOID = {
    'Ulcer': ['alcohol', 'caffeine', 'coffee', 'tea', 'sodas', 'milk', 'sausages', 'fatty meats', 'fry', 'gravy', 'cream soups', 'salad dressing', 'chili peppers',
              'chili', 'horseradish', 'pickles', 'olives', 'fermenet', 'brine', 'chocolate', 'tomatoe', 'lemon', 'orange', 'grapefruit', 'spicy'],
    'Diabetes': ['sugar', 'sweets', 'candy', 'chocolate', 'honey', 'alcohol', 'banana', 'melon', 'mango'],
    'Cholesterol': ['lamb', 'pork', 'butter', 'cream', 'palm oil', 'donuts', 'cakes', 'cake', 'potato chips', 'fried', 'fries', 'cheese', 'sausages', 'bacon', 'hot dogs', 'cookies'],
    'Hypertension':  ['soup', 'pizza', 'sandwich', 'burrito', 'tacos', 'pickle', 'full fat milk', 'full fat cream', 'butter', 'alcohol'],
    'Coronary Heart Disease': ['butter', 'gravy', 'non-dairy creamers', 'fried foods', 'potato chips', 'cookies', 'pies', 'ice cream'],
    'Arthritis': ['soda', 'sweet', 'candy', 'pastries', 'milk', 'donuts', 'fried', 'alcohol', 'wheat', 'barley', 'rye', 'cereal', 'shrimp', 'canned soup', 'pizza', 'bacon']
}


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
        all_foods = pd.DataFrame(Food.fetch_all_foods())
        pd.set_option('display.max_rows', None)
        # Add a filtering condition here - avoid foods based on illness, only if illness is present
        if (user.illness != 'No'):
            print('Filtering foods based on illness: ', user.illness)
            illness_food_avoid = FOODS_AVOID.get(user.illness)
            for index, row in all_foods.iterrows():
                ingredient = [ingredient.strip()
                              for ingredient in row['ingredients'].split(' ')]
                name = [name.strip() for name in row['name'].split(' ')]
                contains = any(item.lower() in illness_food_avoid for item in ingredient) or any(
                    item.lower() in illness_food_avoid for item in name)
                if contains:
                    all_foods.drop(index, inplace=True)
            all_foods.reset_index(drop=True, inplace=True)

        food_choices = choose_foods(
            macro_nutrients_ratio=macro_nutrients_ratio, foods=all_foods)

        temp_id = []
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
                    food_id=food_id, foods_df=all_foods)
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
        rated_food_ids = get_similar_users_recommendations(
            id, ratings, users, all_foods)

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

        if (len(rated_food_choices) != 0):
            hybrid_recommendation_ids = get_hybrid_recommendation(
                similar_users_recommendation_food_ids=rated_food_ids, foods=all_foods, chosen_food_id=temp_id)
        else:
            hybrid_recommendation_ids = similar_food_ids

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


class ScheduleRecommendationResource(Resource):
    # To cache every 24 hours in seconds, timeout = 86400
    @cache.cached(timeout=120)
    def get(self, id):
        default_user_schedule = {
            'Breakfast': [7],
            'Morning': [9, 11],
            'Morning Snacks': [10],
            'Afternoon': [14],
            'Lunch': [13],
            'Afternoon Snacks': [16],
            'Evening': [17],
            'Dinner': [19]
        }

        user_schedule = {
            'Breakfast': [],
            'Morning': [],
            'Morning Snacks': [],
            'Afternoon': [],
            'Lunch': [],
            'Afternoon Snacks': [],
            'Evening': [],
            'Dinner': []
        }

        # Fetch the user's ADL history
        user_adl = ADL.fetch_all_adl_by_id(user_id=id)

        # Train Model for user - predict their meal times and free slots for today
        if len(user_adl) != 0:
            print(
                f"FOUND for user: {id}, ADL history, predicting free times based on this.\n")
            user_adl_df = pd.DataFrame(user_adl)
            # Find free time slots
            free_time_slots = analyse_free_times(
                user_adl_df=user_adl_df, this_activity=['No'])
            free_slots = []
            print()
            print("Finding free slots: \n")

            for _, slot in free_time_slots.iterrows():
                print(f"You might be free at {slot['start_hour']}:00")
                free_slots.append(slot['start_hour'])
                if 6 <= slot['start_hour'] <= 12:
                    user_schedule['Morning'].append(int(
                        slot['start_hour']))
                elif 12 < slot['start_hour'] <= 18:
                    user_schedule['Afternoon'].append(int(
                        slot['start_hour']))
                elif 18 < slot['start_hour'] <= 24:
                    user_schedule['Evening'].append(int(
                        slot['start_hour']))

            user_adl_df = pd.DataFrame(user_adl)
            # Find meal time slots
            meal_time_slots = analyse_free_times(user_adl_df=user_adl_df, this_activity=[
                                                 'Cooking', 'Eat', 'Cook', 'meal_preparation'])
            meal_slots = []
            print()
            print("Finding meal slots: \n")
            for _, slot in meal_time_slots.iterrows():
                print(f"You can eat at {slot['start_hour']}:00")
                meal_slots.append(slot['start_hour'])
                if 7 <= slot['start_hour'] <= 9:
                    user_schedule['Breakfast'].append(int(
                        slot['start_hour']))
                elif 10 <= slot['start_hour'] <= 11:
                    user_schedule['Morning Snacks'].append(int(
                        slot['start_hour']))
                elif 12 <= slot['start_hour'] <= 14:
                    user_schedule['Lunch'].append(int(
                        slot['start_hour']))
                elif 15 <= slot['start_hour'] <= 16:
                    user_schedule['Afternoon Snacks'].append(int(
                        slot['start_hour']))
                elif 17 <= slot['start_hour'] <= 20:
                    user_schedule['Dinner'].append(int(
                        slot['start_hour']))

        else:
            # If no history found return a default schedule
            print(f"ADL history NOT FOUND for user: {id} .\n")
            user_schedule = default_user_schedule

        print(user_schedule)

        # Check if user exists
        db_user = User.fetch_by_id(id=id)
        if db_user is not None:
            # Fetch schedule for user
            schedule = db_user.schedule
            if schedule is None:  # Return default schedule
                schedule = default_user_schedule

        return make_response(jsonify({
            "user_id": id,
            "schedule": user_schedule
        }), 200)


class ActivityRecommendationResource(Resource):
    # To cache every 24 hours in seconds, timeout = 86400
    @cache.cached(timeout=120)
    def get(self, id):

        all_activities = Activity.fetch_all_activities()

        # Filter activities for users based on mobility and dexterity score
        db_user = User.fetch_by_id(id=id)
        db_user_mobilityscore = db_user.mobilityscore
        db_user_dexterityscore = db_user.dexterityscore

        suitable_activities = {
            'Morning': {'Outdoor': [], 'Exercise': [], 'Hobbies': []},
            'Afternoon': {'Reading': [], 'Music': []},
            'Evening': {'Gardening': [], 'Yoga': [], 'Chair Yoga': [], 'TV': []}
        }
        hobbies = []
        outdoor = []
        tv = []
        music = []
        reading = []
        gardening = []
        yoga = []
        chairYoga = []
        exercises = []

        for activity in all_activities:
            activity_mobilityscore = activity['mobilityscore']
            activity_dexterityscore = activity['dexterityscore']

            if (activity_mobilityscore <= db_user_mobilityscore) and (activity_dexterityscore <= db_user_dexterityscore):

                if activity['type'] == 'Hobbies':
                    hobbies.append(activity)

                elif activity['type'] == 'Walking':
                    outdoor.append(activity)

                elif activity['type'] == 'Jogging':
                    outdoor.append(activity)

                elif activity['type'] == 'TV':
                    tv.append(activity)

                elif activity['type'] == 'Music':
                    music.append(activity)

                elif activity['type'] == 'Reading':
                    reading.append(activity)

                elif activity['type'] == 'Gardening':
                    gardening.append(activity)

                elif activity['type'] == 'Yoga':
                    yoga.append(activity)

                elif activity['type'] == 'Chair Yoga':
                    chairYoga.append(activity)

                elif 'exercise' in activity['type']:
                    exercises.append(activity)

        suitable_activities['Morning']['Outdoor'] = outdoor
        suitable_activities['Morning']['Exercise'] = exercises
        suitable_activities['Morning']['Hobbies'] = hobbies
        suitable_activities['Afternoon']['Reading'] = reading
        suitable_activities['Afternoon']['Music'] = music
        suitable_activities['Evening']['Gardening'] = gardening
        suitable_activities['Evening']['TV'] = tv
        suitable_activities['Evening']['Yoga'] = yoga
        suitable_activities['Evening']['Chair Yoga'] = chairYoga

        return make_response(jsonify({
            "user_id": id,
            "activities": suitable_activities
        }), 200)


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
