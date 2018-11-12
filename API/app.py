from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse  
from predict import predict_flight_delay
import os

app = Flask(__name__)  
api = Api(app)


class Prediction(Resource):  
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('AIRLINE', required=True, help="AIRLINE cannot be blank!")
        parser.add_argument('DAY_OF_WEEK', required=True, help="DAY_OF_WEEK cannot be blank!")
        parser.add_argument('MONTH', required=True, help="MONTH cannot be blank!")
        parser.add_argument('ORIGIN_AIRPORT', required=True, help="ORIGIN_AIRPORT cannot be blank!")
        parser.add_argument('DESTINATION_AIRPORT', required=True, help="DESTINATION_AIRPORT cannot be blank!")
        args = parser.parse_args()
        
        x = [[args['AIRLINE'],
              int(args['DAY_OF_WEEK']),
              int(args['MONTH']),
              args['ORIGIN_AIRPORT'],
              args['DESTINATION_AIRPORT']
             ]]
        
        print('FlaskApp', x)
        y_pred, y_prob = predict_flight_delay(x)
        print('FlaskApp', y_pred, y_prob)
        
        return jsonify(AIRLINE=args['AIRLINE'],
                       DAY_OF_WEEK=int(args['DAY_OF_WEEK']),
                       MONTH=int(args['MONTH']),
                       ORIGIN_AIRPORT=args['ORIGIN_AIRPORT'],
                       DESTINATION_AIRPORT=args['DESTINATION_AIRPORT'],
                       PRED_ARRIVAL_DELAY=str(y_pred), 
                       PRED_PROB=str(y_prob))

api.add_resource(Prediction, '/prediction')


if __name__ == '__main__':  
    app.run(debug=False, host=os.environ['MODEL_HOST'])
#     app.run(debug=True)