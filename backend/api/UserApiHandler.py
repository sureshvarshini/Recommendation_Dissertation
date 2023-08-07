from flask_restful import Resource
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, create_access_token, create_refresh_token
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from models.Model import User


class UserResource(Resource):
    @jwt_required()
    def get(self, id):
        db_user = User.fetch_by_id(id=id)

        if db_user is not None:
            return make_response(jsonify({
                "id": db_user.id,
                "Username": db_user.username,
                "Firstname": db_user.firstname,
                "Lastname": db_user.lastname,
                "Email": db_user.email,
                "Age": db_user.age,
                "Gender": db_user.gender,
                "Height": db_user.height,
                "Weight": db_user.weight,
                "Illness": db_user.illness,
            }), 200)

        return make_response(jsonify({
            "message": f"User '{id}' does not exist.",
            "status": 404
        }), 404)

    @jwt_required()
    def put(self, id):
        data = request.get_json()

        db_user = User.fetch_by_id(id=id)

        if db_user is None:
            return make_response(jsonify({
                "message": f"User '{id}' does not exist.",
                "status": 404
            }), 404)

        firstname = data.get("firstname")
        lastname = data.get("lastname")
        age = data.get("age")
        gender = data.get("gender")
        height = data.get("height")
        weight = data.get("weight")
        illness = data.get("illness")

        if firstname:
            db_user.firstname = firstname
        if lastname:
            db_user.lastname = lastname
        if age:
            db_user.age = age
        if gender:
            db_user.gender = gender
        if height:
            db_user.height = height
        if weight:
            db_user.weight = weight
        if illness:
            db_user.illness = illness

        db_user.save()

        return make_response(jsonify({
            "request": data,
            "message": "User details updated successfully!",
            "Status": 200
        }), 200)

    @jwt_required()
    def delete(self, id):
        db_user = User.fetch_by_id(id=id)

        if db_user is None:
            return make_response(jsonify({
                "message": f"User '{id}' does not exist.",
                "status": 404
            }), 404)

        db_user.delete()

        return make_response(jsonify({
            "message": "User deleted successfully. Sorry to see you go :(",
            "status": 200
        }), 200)


class SignupUserResource(Resource):
    def post(self):

        data = request.get_json()

        username = data["username"]
        password = data["password"]
        email = data["email"]
        firstname = data["firstname"]
        lastname = data["lastname"]
        age = data["age"]
        gender = data["gender"]
        height = data["height"]
        weight = data["weight"]
        illness = data["illness"]
        mobilityscore = data["mobilityscore"]

        db_user = User.fetch_by_username(username=username)

        if db_user is not None:
            return make_response(jsonify({
                "message": f"User with username '{username}' already exists. Try again with a different name.",
                "status": 400
            }), 400)

        new_user = User(
            username=username,
            password=generate_password_hash(password),
            email=email,
            firstname=firstname,
            lastname=lastname,
            age=age,
            gender=gender,
            height=height,
            weight=weight,
            illness=illness,
            mobilityscore=mobilityscore
        )

        new_user_id = new_user.save()

        return make_response(jsonify({
            "message": "User created successfuly.",
            "id": new_user_id,
            "status": 201
        }), 201)


class LoginUserResource(Resource):
    def post(self):
        data = request.get_json()

        username = data["username"]
        password = data["password"]

        db_user = User.fetch_by_username(username=username)

        if db_user and check_password_hash(db_user.password, password):

            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)

            return make_response(jsonify({
                "message": "Token generated successfully.",
                "status": 200,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "id": db_user.id
            }), 200)

        else:
            return make_response(jsonify({
                "message": "Incorrect username or password. Please try again.",
                "status": 400
            }), 400)


class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):

        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)

        return make_response(jsonify({
            "message": "Token refreshed successfully.",
            "status": 200,
            "access_token": new_access_token
        }), 200)
