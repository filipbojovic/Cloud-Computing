import tensorflow as tf
import pandas as pd
import numpy as np

""" --------------------- HYPERPARAMETERS --------------------- """
num_of_epochs = 100
num_of_neurons = 20
hidden_layers = 2
activation_function = 'sigmoid'
output_activation = 'softmax'
learning_rate = 0.001

data = pd.read_csv("banknote_dataset.csv")

print(data.head())