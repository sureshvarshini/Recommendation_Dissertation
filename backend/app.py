from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models.Model import db
from api.TestApiHandler import TestApiHandler
from api.UserApiHandler import UserResource, SignupUserResource, LoginUserResource, RefreshResource
from api.RecommendationApiHandler import FoodRecommendationResource, AddRatingResource, ViewRatingResource
from config import Config
from DataCleaning.DataPreprocessing import clean_food_csv, clean_rating_csv
from ImportFood import import_food_csv_data
from ImportRatings import import_rating_csv_data

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)
app.config.from_object(Config)
api = Api(app)

db.init_app(app)
JWTManager(app)

# Clean csv
clean_food_csv()
# Import food csv into database once - if not inserted
print('Importing food csv to SQL database:\n')
csv_file = 'D:\\Varshini\\CourseWork\\Dissertation\\Implementation\\Recommendation_Dissertation\\backend\\DataCleaning\\cleanedDatasets\\nutrition_cleaned.csv'
import_food_csv_data(csv_file)

# Clean csv
clean_rating_csv()
# Import food csv into database once - if not inserted
print('Importing rating csv to SQL database:\n')
csv_file = 'D:\\Varshini\\CourseWork\\Dissertation\\Implementation\\Recommendation_Dissertation\\backend\\DataCleaning\\cleanedDatasets\\ratings_cleaned.csv'
import_rating_csv_data(csv_file)

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