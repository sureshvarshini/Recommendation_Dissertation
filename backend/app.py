from flask import Flask, current_app, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler
from models.Model import db
from api.TestApiHandler import TestApiHandler
from api.UserApiHandler import UserResource, SignupUserResource, LoginUserResource, RefreshResource
from api.RecommendationApiHandler import FoodRecommendationResource, AddRatingResource, ViewRatingResource, ScheduleRecommendationResource, WaterRecommendationResource, ActivityRecommendationResource
from api.ModelApiHandler import ModelTrainingResource
from config import Config
from preprocessing.DataPreprocessing import clean_food_csv, clean_rating_csv
from ImportFood import import_food_csv_data
from ImportRatings import import_rating_csv_data
from ImportActivity import load_history_adl_data, import_activity_csv_data
from ImportWater import reset_water
from caching import cache

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)
app.config.from_object(Config)
app.json.sort_keys = False
api = Api(app)

db.init_app(app)
cache.init_app(app)
JWTManager(app)

# <----- Execute these lines for fresh app start ----->
# clean_food_csv()
# print('Importing food csv to SQL database:\n')
# csv_file = 'D:\\Varshini\\CourseWork\\Dissertation\\Implementation\\Github\\Recommendation_Dissertation\\backend\\preprocessing\\cleanedDatasets\\food_data_cleaned.csv'
# import_food_csv_data(csv_file)

# clean_rating_csv()
# print('Importing rating csv to SQL database:\n')
# csv_file = 'D:\\Varshini\\CourseWork\\Dissertation\\Implementation\\Github\\Recommendation_Dissertation\\backend\\preprocessing\\cleanedDatasets\\ratings_cleaned.csv'
# import_rating_csv_data(csv_file)

# print('Importing activity csv to SQL database:\n')
# csv_file = 'D:\\Varshini\\CourseWork\\Dissertation\\Implementation\\Github\\Recommendation_Dissertation\\backend\\preprocessing\\cleanedDatasets\\Activities\\activity_cleaned.csv'
# import_activity_csv_data(csv_file)
# <----- Till here ----->

# Train model from history data - at the beginning of the application
# load_history_adl_data()


@app.route("/", defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


# Scheduler to reset water intake every 24 hours (hours=24)
# To show it working, it is set to every 5 mins
water_reset_scheduler = BackgroundScheduler(daemon=True)
water_reset_scheduler.add_job(reset_water, 'interval', minutes=5)
water_reset_scheduler.start()

api.add_resource(TestApiHandler, '/test')
api.add_resource(UserResource, '/user/<int:id>')
api.add_resource(SignupUserResource, '/user/signup')
api.add_resource(LoginUserResource, '/user/login')
api.add_resource(RefreshResource, '/user/token/refresh')
api.add_resource(FoodRecommendationResource, '/recommend/<int:id>/foods')
api.add_resource(AddRatingResource, '/ratings')
api.add_resource(ViewRatingResource, '/ratings/<int:id>/<int:food_id>')
api.add_resource(ScheduleRecommendationResource, '/schedule/<int:id>')
api.add_resource(ActivityRecommendationResource, '/activity/<int:id>')
api.add_resource(WaterRecommendationResource, '/water/<int:id>')
api.add_resource(ModelTrainingResource, '/model')