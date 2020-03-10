from app import api, db

from flask import jsonify
from flask_restful import Resource, reqparse
from dateutil.parser import parse as date_parser

from app.models import SensorData, SensorDataTest, SensorDataSchema

data_schema = SensorDataSchema(many=True)

class Heartbeat(Resource):
    def get(self):
        return {'STATUS': 'OK', 'message': 'Server is running ok :)'}

api.add_resource(Heartbeat, '/', endpoint="heartbeat")

class DataPointList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('datapoints', type = list, required=True, help="No data provided", location = 'json')

    def get(self, table='live', gait = None):

        if table == 'test':
            if gait:
                data = SensorDataTest.query.filter_by(gait=gait).all()
            else:
                data = SensorDataTest.query.all()
        else:
            if gait:
                data = SensorData.query.filter_by(gait=gait).all()
            else:
                data = SensorData.query.all()

        return {'STATUS': 'OK', 'payload': data_schema.dump(data)}, 200

    def post(self, table = 'live', gait = None):
        args = self.reqparse.parse_args()

        for data in args['datapoints']:
            if table == 'test':
                data = SensorDataTest(
                    activity_id = data['activity_id'],
                    gait = data['gait'],
                    timestamp = data['timestamp'],
                    acc_x = data['raw_data']['acc']['x'],
                    acc_y = data['raw_data']['acc']['y'],
                    acc_z = data['raw_data']['acc']['z'],
                    gyr_x = data['raw_data']['gyr']['x'],
                    gyr_y = data['raw_data']['gyr']['y'],
                    gyr_z = data['raw_data']['gyr']['z'],
                    mag_x = data['raw_data']['mag']['x'],
                    mag_y = data['raw_data']['mag']['y'],
                    mag_z = data['raw_data']['mag']['z']
                )
            else:
                data = SensorData(
                    activity_id = data['activity_id'],
                    gait = data['gait'],
                    timestamp = data['timestamp'],
                    acc_x = data['raw_data']['acc']['x'],
                    acc_y = data['raw_data']['acc']['y'],
                    acc_z = data['raw_data']['acc']['z'],
                    gyr_x = data['raw_data']['gyr']['x'],
                    gyr_y = data['raw_data']['gyr']['y'],
                    gyr_z = data['raw_data']['gyr']['z'],
                    mag_x = data['raw_data']['mag']['x'],
                    mag_y = data['raw_data']['mag']['y'],
                    mag_z = data['raw_data']['mag']['z']
                )
            try:
                db.session.add(data)
            except Exception as e:
                return { 'STATUS': 'ERROR', 'message': 'Database error' }, 500
        
        try:
            db.session.commit()
        except Exception as e:
            return { 'STATUS': 'ERROR', 'message': 'Database error' }

        return {'STATUS': 'OK', 'message': 'Saved {} datapoints'.format(len(args['datapoints']))}


api.add_resource(DataPointList, '/data', endpoint="datapoints")
api.add_resource(DataPointList, '/data/<int:gait>', endpoint="datapoints-gait")
api.add_resource(DataPointList, '/data/<string:table>', endpoint="datapoints-table")
api.add_resource(DataPointList, '/data/<string:table>/<int:gait>', endpoint="datapoints-table-gait")