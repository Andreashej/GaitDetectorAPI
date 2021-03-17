import matplotlib.pyplot as plt
import numpy as np

import DataProcessor as dp

from app.models import SensorData, SensorDataTest
from app import create_app, db

application = create_app()
application.app_context().push()

# data = dp.get_dataset_windowed(200,4, include=["751a0113-2298-462e-a718-770f336cd5d1"], random=False, gaits=[0], exclude_features=['acc_y', 'acc_z', 'gyr_x', 'gyr_y', 'gyr_z', 'mag_x', 'mag_y', 'mag_z'])


for i in range(0,1000):
    data = SensorData.query.with_entities(SensorData.acc_z, SensorData.timestamp).filter_by(gait=0).limit(200).offset(5000 + i * 4).all()
    x_axis = list()
    values = list()
    starttime = data[0].timestamp
    for j, dp in enumerate(data):
        x_axis.append(dp.timestamp - starttime)
        values.append(dp.acc_z)

    plt.figure('Z-axis Acceleration')
    plt.ylim(-1.5,0.75)
    plt.plot(x_axis, values)
    plt.axis('off')
    print(i)
    plt.savefig('plots/walk_{}.png'.format(i), dpi=300, bbox_inches='tight')
    # plt.show()
    plt.clf()

# plt.figure('Acceleration data: Tolt')

# plt.subplot()
# plt.plot(x_axis, acc_x)

# plt.subplot()
# plt.plot(x_axis, acc_y, label="gyr_y")

# plt.subplot()
# plt.plot(x_axis, acc_z, label="gyr_z")

# plt.ylabel('gyr')
# plt.xlabel('Time')
# plt.legend()

# plt.show()