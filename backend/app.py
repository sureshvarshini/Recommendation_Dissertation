from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models.User import db
from api.TestApiHandler import TestApiHandler
from api.UserApiHandler import UserResource, SignupUserResource, LoginUserResource, RefreshResource
from config import Config

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)
app.config.from_object(Config)
api = Api(app)

db.init_app(app)
JWTManager(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(TestApiHandler, '/test')
api.add_resource(UserResource, '/user/<int:id>')
api.add_resource(SignupUserResource, '/user/signup')
api.add_resource(LoginUserResource, '/user/login')
api.add_resource(RefreshResource, '/user/token/refresh')