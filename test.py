from keras import Sequential
from keras.layers import LSTM, Dropout, Dense

import numpy as np

from DataProcessor import get_dataset_windowed

def create_baseline_lstm(sample_size):
    model = Sequential()
    model.add(LSTM(100, input_shape=(sample_size,9)))
    model.add(Dropout(0.2))
    model.add(Dense(10, input_dim=9, kernel_initializer='normal', activation = 'relu'))
    model.add(Dropout(0.2))
    model.add(Dense(5, kernel_initializer='normal', activation = 'softmax'))

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"] )

    return model

def get_label_text(num):
    labels = ['walk', 'tolt', 'trot', 'canter', 'pace']

    return labels[num]

model = create_baseline_lstm(200)

model.load_weights("model-030-0.973062-0.971129.h5")

dataset = get_dataset_windowed(200, 50, include=["2c438fb1-e10e-41d8-a194-69544afdad20"], randomize=False)

labels = model.predict(dataset[0])

for i, label in enumerate(labels):
    index = np.argmax(label)
    truth_index = np.argmax(dataset[1][i])
    print(f"Prediction: {get_label_text(index)}, Actual: {get_label_text(truth_index)}")