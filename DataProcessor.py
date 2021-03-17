import pandas as pd
import numpy as np
from sqlalchemy import func, and_
import math

from app.models import SensorData
from app import create_app, db

application = create_app()
application.app_context().push()

feature_indices = {
    "acc_x": 0,
    "acc_y": 1,
    "acc_z": 2,
    "gyr_x": 3,
    "gyr_y": 4,
    "gyr_z": 5,
    "mag_x": 6,
    "mag_y": 7,
    "mag_z": 8,
}

def get_label(gait):
    if gait == 0:
        return [1, 0, 0, 0, 0]
    elif gait == 1:
        return [0, 1, 0, 0, 0]
    elif gait == 2:
        return [0, 0, 1, 0, 0]
    elif gait == 3:
        return [0, 0, 0, 1, 0]
    else:
        return [0, 0, 0, 0, 1]

def windowize(dataset, window_size = 200, step = 200):
    X = dataset[:,3:12].astype(float)
    label = get_label(dataset[:,2][0])

    windows_count = math.floor((len(X) - window_size) / step)+1
    
    Y = list()
    windows = list()

    for i in range(0, windows_count):
        Y.append(label)

        min_index = i * step
        max_index = min_index + window_size

        window = X[min_index:max_index]

        windows.append(window)
    
    Y =  np.array(Y)
    windows = np.array(windows)

    return windows, Y

def randomize(dataset, *args):
    permutation = np.random.permutation(dataset.shape[0])
    data = dataset[permutation]

    return_sets = [data]
    for ds in args:
        return_sets.append(ds[permutation])

    return return_sets

def get_dataset_windowed(window_size = 200, step = 200, **kwargs):
    exclude = kwargs.get("exclude", [])
    include = kwargs.get("include", [])
    random = kwargs.get("randomize", True)
    gaits = kwargs.get("gaits", [0,1,2,3])

    features = kwargs.get("exclude_features", [])

    if include:
        activities = SensorData.query.with_entities(SensorData.activity_id, func.count(SensorData.activity_id).label("datapoints")).group_by(SensorData.activity_id).having(and_(func.count(SensorData.activity_id) > 200, SensorData.activity_id.in_(include))).all()
    else:
        activities = SensorData.query.with_entities(SensorData.activity_id, func.count(SensorData.activity_id).label("datapoints")).group_by(SensorData.activity_id).having(and_(func.count(SensorData.activity_id) > 200, SensorData.activity_id.notin_(exclude))).all()

    X = np.empty((0,window_size,9))
    Y = np.empty((0,5))

    for activity in activities:
        if 0 in gaits:
            walk = pd.read_sql(SensorData.query.filter_by(activity_id = activity.activity_id, gait = 0).offset(500).statement, db.engine)
        if 1 in gaits:
            tolt = pd.read_sql(SensorData.query.filter_by(activity_id = activity.activity_id, gait = 1).statement, db.engine)
        if 2 in gaits:
            trot = pd.read_sql(SensorData.query.filter_by(activity_id = activity.activity_id, gait = 2).statement, db.engine)
        if 3 in gaits and activity.activity_id not in ["85a256d2-40f3-4ae1-a688-33a2883ef7ae","d60eecdc-3869-4f7c-a7d8-678f2e2ea4e1", "c300f5cf-aae7-4e7d-86d0-029fa1cc9ff8","e64fe66d-a3b1-4ebb-8cdf-c5b9320b1123"]:
            canter = pd.read_sql(SensorData.query.filter_by(activity_id = activity.activity_id, gait = 3).statement, db.engine)

        # print("Activity: {}, Walk: {}, Tolt: {}, Trot: {}, Canter: {}".format(activity.activity_id, len(walk), len(tolt), len(trot), len(canter)))

        X_walk = np.empty((0,window_size,9))
        Y_walk = np.empty((0,5))
        X_tolt = np.empty((0,window_size,9))
        Y_tolt = np.empty((0,5))
        X_trot = np.empty((0,window_size,9))
        Y_trot = np.empty((0,5))
        X_canter = np.empty((0,window_size,9))
        Y_canter = np.empty((0,5))

        if 0 in gaits:
            X_walk, Y_walk = windowize(walk.values, window_size, step)
        if 1 in gaits:
            X_tolt, Y_tolt = windowize(tolt.values, window_size, step)
        if 2 in gaits:
            X_trot, Y_trot = windowize(trot.values, window_size, step)
        if 3 in gaits and activity.activity_id not in ["85a256d2-40f3-4ae1-a688-33a2883ef7ae","d60eecdc-3869-4f7c-a7d8-678f2e2ea4e1", "c300f5cf-aae7-4e7d-86d0-029fa1cc9ff8","e64fe66d-a3b1-4ebb-8cdf-c5b9320b1123"]:
            X_canter, Y_canter = windowize(canter.values, window_size, step)

        X = np.vstack((X, X_walk, X_tolt, X_trot, X_canter))
        Y = np.vstack((Y, Y_walk, Y_tolt, Y_trot, Y_canter))
        # print(activity.activity_id)

    X = np.delete(X, [feature_indices[feature] for feature in features], axis=2)

    if random:
        dataset = randomize(X, Y)
    else:
        dataset = [X, Y]

    return dataset

def get_dataset_flat(**kwargs):

    exclude = kwargs.get("exclude", [])
    include = kwargs.get("include", [])

    if include:
        activities = SensorData.query.with_entities(SensorData.activity_id, func.count(SensorData.activity_id).label("datapoints")).group_by(SensorData.activity_id).having(and_(func.count(SensorData.activity_id) > 200, SensorData.activity_id.in_(include))).all()
    else:
        activities = SensorData.query.with_entities(SensorData.activity_id, func.count(SensorData.activity_id).label("datapoints")).group_by(SensorData.activity_id).having(and_(func.count(SensorData.activity_id) > 200, SensorData.activity_id.notin_(exclude))).all()

    X = np.empty((0,9))
    Y = np.empty((0,5))
    for activity in activities:
        dps = pd.read_sql(SensorData.query.filter_by(activity_id = activity.activity_id).statement, db.engine)

        X_new = np.array(dps.values[:,3:12].astype(float))
        Y_new = list()
        
        for label in dps.values[:,2]:
            label = get_label(label)
            Y_new.append(label)


        X = np.vstack((X, X_new))
        Y = np.vstack((Y, Y_new))

    dataset = randomize(X, Y)

    return dataset

def get_unique_activities():
    ids = SensorData.query.with_entities(SensorData.activity_id).group_by(SensorData.activity_id).having(func.count(SensorData.activity_id) > 200).all()
    return map(lambda data: data.activity_id, ids)