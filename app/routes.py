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

        successful = []

        for data in args['datapoints']:
            if data:
                if table == 'test':
                    db_data = SensorDataTest(
                        activity_id = data['activity_id'],
                        gait = data['gait'],
                        timestamp = data['timestamp'],
                        acc_x = data['acc_x'],
                        acc_y = data['acc_y'],
                        acc_z = data['acc_z'],
                        gyr_x = data['gyr_x'],
                        gyr_y = data['gyr_y'],
                        gyr_z = data['gyr_z'],
                        mag_x = data['mag_x'],
                        mag_y = data['mag_y'],
                        mag_z = data['mag_z'],
                        setting = data['setting'],
                        phone_placement = data['position']
                    )
                else:
                    db_data = SensorData(
                        activity_id = data['activity_id'],
                        gait = data['gait'],
                        timestamp = data['timestamp'],
                        acc_x = data['acc_x'],
                        acc_y = data['acc_y'],
                        acc_z = data['acc_z'],
                        gyr_x = data['gyr_x'],
                        gyr_y = data['gyr_y'],
                        gyr_z = data['gyr_z'],
                        mag_x = data['mag_x'],
                        mag_y = data['mag_y'],
                        mag_z = data['mag_z'],
                        setting = data['setting'],
                        phone_placement = data['position']
                    )
                try:
                    db.session.add(db_data)
                    successful.append(data['id'])
                except Exception as e:
                    return { 'STATUS': 'ERROR', 'message': 'Database error' }, 500
        
        try:
            db.session.commit()
        except Exception as e:
            return { 'STATUS': 'ERROR', 'message': 'Database error' }

        return {'STATUS': 'OK', 'message': 'Saved {} datapoints'.format(len(successful)), 'payload': successful}


api.add_resource(DataPointList, '/data', endpoint="datapoints")
api.add_resource(DataPointList, '/data/<int:gait>', endpoint="datapoints-gait")
api.add_resource(DataPointList, '/data/<string:table>', endpoint="datapoints-table")
api.add_resource(DataPointList, '/data/<string:table>/<int:gait>', endpoint="datapoints-table-gait")