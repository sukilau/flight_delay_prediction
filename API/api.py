from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse  
from utils.predict import predict_user_gender


app = Flask(__name__)  
api = Api(app)


class Prediction(Resource):  
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid', required=True, help="uid cannot be blank!")
        args = parser.parse_args()
        y_gender, y_prob = predict_user_gender(args['uid'])
        return jsonify(uid=args['uid'], predicted_gender=y_gender, probability=round(y_prob,2))

api.add_resource(Prediction, '/prediction')


if __name__ == '__main__':  
    app.run(debug=False)