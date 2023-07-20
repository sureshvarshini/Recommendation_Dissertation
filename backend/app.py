from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models.Model import db
from api.TestApiHandler import TestApiHandler
from api.UserApiHandler import UserResource, SignupUserResource, LoginUserResource, RefreshResource
from api.RecommendationApiHandler import FoodRecommendationResource, AddRatingResource, ViewRatingResource, ActivityRecommendationResource, WaterRecommendationResource
from config import Config
from preprocessing.DataPreprocessing import clean_food_csv, clean_rating_csv
from ImportFood import import_food_csv_data
from ImportRatings import import_rating_csv_data

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)
app.config.from_object(Config)
app.json.sort_keys = False
api = Api(app)

db.init_app(app)
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
# <----- Till here ----->

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(TestApiHandler, '/test')
api.add_resource(UserResource, '/user/<int:id>')
api.add_resource(SignupUserResource, '/user/signup')
api.add_resource(LoginUserResource, '/user/login')
api.add_resource(RefreshResource, '/user/token/refresh')
api.add_resource(FoodRecommendationResource, '/recommend/<int:id>/foods')
api.add_resource(AddRatingResource, '/ratings')
api.add_resource(ViewRatingResource, '/ratings/<int:id>')
api.add_resource(ActivityRecommendationResource, '/activity/<int:id>')
api.add_resource(WaterRecommendationResource, '/water/<int:id>')