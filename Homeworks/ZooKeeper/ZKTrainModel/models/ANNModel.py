import tensorflow as tf
import uuid
import os
import config
import pandas as pd
from tensorflow import keras
from keras import activations, optimizers, layers, Sequential
from keras.models import load_model
from database import Db
from sklearn.model_selection import train_test_split

class ANN:
    
    def __init__(self, optimizer, batch_size, num_of_epochs, activation, output_activation, model_name):
        self._optimizer = optimizer
        self._batch_size = batch_size
        self._num_of_epochs = num_of_epochs
        self._activation = activation
        self._output_activation = output_activation
        self._dataset_name = model_name # ovo sam naknadno dodao kod zookeepera jer mi je sada potrebno da se dataset cuva.
        self._model_name = model_name +"_" +optimizer +"_" +str(batch_size) +"_activation:" +activation  +"_epochs:" +str(num_of_epochs)
        self._neurons_per_hidden_layer = [10, 10]

        self._init_default_hyperparameters()

    def _create_model(self, num_of_inputs, num_of_outputs):
        self.model = Sequential()
        
        self.model.add(layers.Input(shape = (num_of_inputs, )))
        for unit in self._neurons_per_hidden_layer:
            self.model.add(layers.Dense(units = int(unit), activation = self._activation))
        self.model.add(layers.Dense(units = num_of_outputs, activation = self._output_activation))

        self.model.compile(optimizer = self._optimizer, loss = 'mse', metrics = ['accuracy', 'AUC'])

    def train_model(self, data, num_of_outputs):
        
        """ -------------- SPLIT DATA -------------- """
        data = pd.read_csv(data)
        data = data.sample(frac = 1)

        # SAMO AKO NE POSTOJI OVAJ FAJL
        if not os.path.isfile(os.path.join(config.datasets_path, self._dataset_name)):
            data.to_csv(os.path.join(config.datasets_path, self._dataset_name) +".csv", index = False)

        X, y = data.values[:, :-num_of_outputs], data.values[:, -num_of_outputs]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, shuffle = False)
        
        self._create_model(len(data.columns) - num_of_outputs, num_of_outputs)

        self.model.fit(X_train, y_train, batch_size = self._batch_size, epochs = self._num_of_epochs, verbose = 0)

        model_guid = self.save_model()
        metrics = self._evaluate_model(X_test, y_test)

        db = Db.getInstance()
        db.add_model(self._model_name, self._dataset_name, metrics["mse"], metrics["auc"], metrics["acc"], os.path.join(model_guid, self._model_name))

        return metrics

    def predict(model, dataset, num_of_outputs):

        X_test = pd.read_csv(dataset)
        X_test = X_test.values[:, :-num_of_outputs]
        return model.predict(X_test)

    def _evaluate_model(self, X_val, y_true):
        mse, acc, auc = self.model.evaluate(X_val, y_true, verbose = 0)
        return {
            "mse": mse,
            "acc": acc,
            "auc": auc
        }

    def save_model(self):

        guid = uuid.uuid1()
        guid = str(guid)
        os.mkdir(os.path.join(config.storage_path, guid))
        self.model.save(os.path.join(config.storage_path, guid, self._model_name))

        return guid

    def load_model(model_path):
        return load_model(os.path.join(config.storage_path, model_path))
        # return tf.saved_model.load(os.path.join(config.storage_path, model_path))

    def evaluate_existing_model(model_path, dataset, num_of_outputs):
        model = ANN.load_model(model_path)

        X, y = dataset.values[:, :-num_of_outputs], dataset.values[:, -num_of_outputs]
        _, X_test, _, y_test = train_test_split(X, y, test_size = 0.3, shuffle = False)

        mse, acc, auc = model.evaluate(X_test, y_test, verbose = 0)
        return mse, acc, auc

    def _init_default_hyperparameters(self):
        if self._optimizer is None:
            self._optimizer = 'Adam'
        if self._batch_size is None:
            self._batch_size = 32
        if self._num_of_epochs is None:
            self._num_of_epochs = 5
        if self._activation is None:
            self._activation = 'sigmoid'
        if self._output_activation is None:
            self._output_activation = 'sigmoid'