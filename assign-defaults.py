import matplotlib.pyplot as plt

from app.models import SensorData, SensorDataTest
from app import create_app, db

application = create_app()
application.app_context().push()

data = SensorData.query.update({SensorData.phone_placement: 0, SensorData.setting: 0})

db.session.commit()