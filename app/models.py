from app import db, ma

from marshmallow import fields

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.String(64))
    gait = db.Column(db.Integer)
    acc_x = db.Column(db.Float)
    acc_y = db.Column(db.Float)
    acc_z = db.Column(db.Float)
    gyr_x = db.Column(db.Float)
    gyr_y = db.Column(db.Float)
    gyr_z = db.Column(db.Float)
    mag_x = db.Column(db.Float)
    mag_y = db.Column(db.Float)
    mag_z = db.Column(db.Float)
    timestamp = db.Column(db.BigInteger)

    def __repr__(self):
        return '<SensorData gait:{} >'.format(self.gait)
    
class SensorDataSchema(ma.ModelSchema):
    class Meta:
        model = SensorData

class SensorDataTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.String(64))
    gait = db.Column(db.Integer)
    acc_x = db.Column(db.Float)
    acc_y = db.Column(db.Float)
    acc_z = db.Column(db.Float)
    gyr_x = db.Column(db.Float)
    gyr_y = db.Column(db.Float)
    gyr_z = db.Column(db.Float)
    mag_x = db.Column(db.Float)
    mag_y = db.Column(db.Float)
    mag_z = db.Column(db.Float)
    timestamp = db.Column(db.BigInteger)

    def __repr__(self):
        return '<SensorTestData gait:{} >'.format(self.gait)