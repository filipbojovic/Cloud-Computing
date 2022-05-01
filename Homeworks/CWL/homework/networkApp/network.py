import tensorflow as tf
from tensorflow.keras import Sequential, activations
from tensorflow.keras.layers import Dense
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
import sys

""" --------------------- HYPERPARAMETERS --------------------- """
activation_function = 'relu'
output_activation = 'sigmoid'
learning_rate = 0.001
metrics_callback = ['accuracy', 'AUC']

dataset_path = "/app/banknote_dataset.csv"
""" --------------------- CWL PARAMS --------------------- """
num_of_folds = int(sys.argv[1])
current_fold = int(sys.argv[2])
num_of_epochs = int(sys.argv[3])
batch_size = int(sys.argv[4])
optimizer = sys.argv[5]
hidden_layers = int(sys.argv[6])

""" --------------------- TRAIN AND VAL DATA --------------------- """
data = pd.read_csv(dataset_path)
data = data.sample(frac = 1)

features, targets = data.values[:, :-1], data.values[:, -1]

kf = KFold(n_splits = num_of_folds, shuffle = True, random_state = 1231)
train, val = list(kf.split(features, targets))[current_fold] # train i val sadrze indekse uzoraka koji se koriste

""" --------------------- MODEL DEFINITION --------------------- """
model = Sequential()
model.add(Dense(units = 10, activation = activation_function, input_dim = features.shape[1]))
for i in range(hidden_layers - 1):
    model.add(Dense(units = 10, activation = activation_function))
model.add(Dense(units = 1, activation = output_activation))

model.compile(optimizer = optimizer, loss = 'binary_crossentropy', metrics = metrics_callback)

""" --------------------- MODEL TRAINING --------------------- """
model.fit(features[train, :], targets[train], batch_size = batch_size, epochs = num_of_epochs, verbose = 0)

""" --------------------- EVALUATING MODEL --------------------- """
_, acc, auc = model.evaluate(features[val, :], targets[val], verbose = 0)
print("K =", current_fold, "ACC =", acc, "AUC =", auc)