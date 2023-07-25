import os
from flask import request, jsonify, make_response
from flask_restful import Resource
from recommendation.ActivityLevel import append_data, clean_adl_data

UPLOAD_FILE_LOCATION = os.getcwd(
) + "\\preprocessing\\datasets\\Activity_predictor\\request\\"

class ModelTrainingResource(Resource):
    def post(self):

        if 'file' not in request.files:
            return make_response(jsonify({
            "message": "No file found.",
            "status": 400
        }), 400)

        file = request.files['file']
        # Save the file
        file.save(os.path.join(UPLOAD_FILE_LOCATION, file.filename))

        # append_data(file)
        clean_adl_data(file_name=file.filename)

        return make_response(jsonify({
            "message": "File uploaded onto system successfully.",
            "status": 201
        }), 201)
