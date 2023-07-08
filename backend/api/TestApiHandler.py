from flask_restful import Resource


class TestApiHandler(Resource):
    def get(self):
        return {
            'status': 'SUCCESS',
            'message': 'Hello, welcome to test page of Recommendation application'
        }
