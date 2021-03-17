import numpy as np

import DataProcessor as dp

import tensorflow as tf
from keras.models import load_model
from keras import Sequential
from keras.layers import LSTM, Dense, Dropout, Embedding
from keras.utils import np_utils
from keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
import math

import itertools

es = EarlyStopping('val_loss', min_delta=.01, patience=5, mode='min', verbose=1)
# checkpoint = ModelCheckpoint('model_leave_out-{epoch:03d}-{accuracy:03f}-{val_accuracy:03f}.h5', verbose=1, monitor='val_loss',save_best_only=True, mode='auto')
callbacks = [es]

def create_baseline_dnn():
    model = Sequential()
    model.add(Dense(12, input_dim=9, kernel_initializer='normal', activation = 'relu'))
    model.add(Dropout(0.2))
    model.add(Dense(8, kernel_initializer='normal', activation = 'relu'))
    model.add(Dropout(0.2))
    model.add(Dense(5, kernel_initializer='normal', activation = 'softmax'))

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"] )

    return model

def create_baseline_lstm(input_shape):
    model = Sequential()
    model.add(LSTM(200, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(Dense(10, input_dim=9, kernel_initializer='normal', activation = 'relu'))
    model.add(Dropout(0.2))
    # model.add(Dense(10, kernel_initializer='normal', activation = 'relu'))
    # model.add(Dropout(0.2))
    model.add(Dense(5, kernel_initializer='normal', activation = 'softmax'))

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"] )

    return model

def train_model_lstm(window_size=200, step_size=150):
    data = dp.get_dataset_windowed(window_size,step_size)

    model = create_baseline_lstm(data[0][0].shape)

    history = model.fit(data[0], data[1], batch_size=64, epochs=100, validation_split = 0.2, verbose = 0, callbacks=callbacks)

    model.save("model_lstm.h5")

    file = open("results.txt", "a")
    file.writelines(['RNN results: \n', 'Topology: [LSTM(200),Dense(10)] \n', 'Accuracy: {} \n'.format(history.history['accuracy'][-1]), 'Val accuracy: {} \n'.format(history.history['val_accuracy'][-1]), 'Loss: {} \n'.format(history.history['loss'][-1]), 'Val loss: {} \n'.format(history.history['val_loss'][-1]), '\n'])
    file.close()

    return model

def train_model_dnn():
    data = dp.get_dataset_flat()

    model = create_baseline_dnn()

    history = model.fit(data[0], data[1], batch_size=64, epochs=100, validation_split = 0.2, verbose = 0, callbacks=callbacks)

    model.save("model_dnn.h5")

    file = open("results.txt", 'a')
    file.writelines(['DNN results: \n', 'Accuracy: {} \n'.format(history.history['accuracy'][-1]), 'Val accuracy: {} \n'.format(history.history['val_accuracy'][-1]), 'Loss: {} \n'.format(history.history['loss'][-1]), 'Val loss: {} \n'.format(history.history['val_loss'][-1]),'\n'])
    file.close()

    return model

def compute_confusion_matrix(model):
    data = dp.get_dataset_windowed(200,150)
    y_pred = model.predict(data[0])

    cm = confusion_matrix(data[1].argmax(axis=1), y_pred.argmax(axis=1))
    print(cm)
    plt.matshow(cm, cmap='Blues')
    plt.title("Confusion Matrix")
    plt.ylabel("True label")
    plt.xlabel("Predicted label")

    classes = ["Walk", "Tölt", "Trot", "Canter"]
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        # if normalize:
        #     plt.text(j, i, "{:0.4f}".format(cm[i, j]),
        #              horizontalalignment="center",
        #              color="white" if cm[i, j] > thresh else "black")
        # else:
        plt.text(j, i, "{:,}".format(cm[i, j]),
                    horizontalalignment="center",
                    color="white" if cm[i, j] > thresh else "black")

    plt.show()

    res = model.evaluate(data[0], data[1])

    print(res)


def train_loocv():
    folds = dp.get_unique_activities()
    fold_no = 1

    train_acc = list()
    val_acc = list()

    fold_acc = list()
    fold_loss = list()

    for fold in folds:
        train = dp.get_dataset_windowed(200,150,exclude=[fold])
        model = create_baseline_lstm(train[0][0].shape)
        print('------------------------------------------------------------------------')
        print(f'Training for fold {fold_no} ...')
        history = model.fit(train[0], train[1], batch_size=64, epochs=100, validation_split = 0.2, verbose = 1, callbacks=callbacks)

        test = dp.get_dataset_windowed(200,150,include=[fold])
        scores = model.evaluate(test[0], test[1])

        train_acc.append(history.history.get('accuracy')[-1]*100)
        val_acc.append(history.history.get('val_accuracy')[-1]*100)

        fold_acc.append(scores[1] * 100)
        fold_loss.append(scores[0])

        print(f'Score for fold {fold_no}: {model.metrics_names[0]} of {scores[0]}; {model.metrics_names[1]} of {scores[1]*100}%')

        fold_no = fold_no + 1

    print('------------------------------------------------------------------------')
    print('Score per fold')
    for i in range(0, len(fold_acc)):
        print('------------------------------------------------------------------------')
        print(f'> Fold {i+1} - Loss: {fold_loss[i]} - Accuracy: {fold_acc[i]}%')
    
    print('------------------------------------------------------------------------')
    print('Average scores for all folds:')
    print(f'> Accuracy: {np.mean(fold_acc)} (+- {np.std(fold_acc)})')
    print(f'> Loss: {np.mean(fold_loss)}')
    print(f'> Max accuracy: {np.amax(fold_acc)}')
    print(f'> Min loss: {np.amin(fold_loss)}')
    print(f'> Min accuracy: {np.amin(fold_acc)}')
    print(f'> Max loss: {np.amax(fold_loss)}')
    print('------------------------------------------------------------------------')

    max_fold = range(1,len(fold_acc) + 1)

    plt.plot(max_fold, fold_acc, label="Evaluation")
    plt.plot(max_fold, train_acc, label="Training")
    plt.plot(max_fold, val_acc, label="Validation")
    plt.title("Leave-one-out Cross Validation results")
    plt.ylabel("Accuracy")
    plt.xlabel("Fold #")
    plt.axis([1,len(fold_acc),0,100])
    plt.xticks(max_fold)
    plt.legend()
    plt.show()

# model = train_model()
model = load_model("model_dnn.h5")

# train_loocv()



# dnn = train_model_dnn()

# rnn = train_model_lstm(200,100)

# train_model_lstm(200,200)
# train_model_lstm(200,150)
# train_model_lstm(200,100)
# train_model_lstm(200,50)
# train_model_lstm(100,50)
# train_model_lstm(100,25)
# train_model_lstm(50,25)

train_model_lstm()