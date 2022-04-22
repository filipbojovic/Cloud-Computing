import tensorflow as tf
from tensorflow.keras import Sequential, activations
from tensorflow.keras.layers import Dense
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
import sys

""" --------------------- HYPERPARAMETERS --------------------- """
hidden_layers = 1
batch_size = 32
activation_function = 'relu'
optimizer = 'adam'
output_activation = 'sigmoid'
learning_rate = 0.001
metrics_callback = ['accuracy', 'AUC']

""" --------------------- CWL PARAMS --------------------- """
num_of_folds = int(sys.argv[1])
current_fold = int(sys.argv[2])
dataset_path = sys.argv[3]
num_of_epochs = int(sys.argv[4])

# num_of_folds = 10
# current_fold = 2
# dataset_path = "banknote_dataset.csv"

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