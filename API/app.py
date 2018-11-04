from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse  
from utils.predict import predict_flight_delay


app = Flask(__name__)  
api = Api(app)


class Prediction(Resource):  
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('AIRLINE', required=True, help="AIRLINE cannot be blank!")
        parser.add_argument('DAY_OF_WEEK', required=True, help="DAY_OF_WEEK cannot be blank!")
        parser.add_argument('DEPARTURE_TIME', type=float, required=True, help="DEPARTURE_TIME cannot be blank!")
        parser.add_argument('DISTANCE', type=float, required=True, help="DISTANCE cannot be blank!")
        args = parser.parse_args()
        x = [[args['AIRLINE'],args['DAY_OF_WEEK'],args['DEPARTURE_TIME'],args['DISTANCE']]]
        y_pred, y_prob = predict_flight_delay(x)
        return jsonify(AIRLINE=args['AIRLINE'], DAY_OF_WEEK=args['DAY_OF_WEEK'], DEPARTURE_TIME=args['DEPARTURE_TIME'], DISTANCE=args['DISTANCE'], Predicted_Delay=str(y_pred), Prob=str(y_prob))

api.add_resource(Prediction, '/prediction')


if __name__ == '__main__':  
    app.run(debug=False)