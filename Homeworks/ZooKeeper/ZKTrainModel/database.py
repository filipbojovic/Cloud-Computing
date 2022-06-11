import os
import mysql.connector
import config
from models.fastAPIModel import ModelAPI

class Db():
    __instance = None

    def __init__(self):
        self._db = mysql.connector.connect(user = config.user, password = config.password, host = config.host, database = config.db_name, port = config.port)
        self._dbh = self._db.cursor()
        self._create_table()
        Db.__instance = self

    @staticmethod
    def getInstance():
        if Db.__instance == None:
            Db()
        return Db.__instance
    
    def get_all_models(self):
        sql = "select * from models"
        
        self._dbh.execute(sql)
        records = self._dbh.fetchall()
        
        models = []
        for row in records:
            path = row[6]
            model_name = path.split('/')[1]
            dataset_name = row[2]
            models.append(ModelAPI(model_id = row[0], model_name = model_name, dataset_name = dataset_name, mse = row[3], auc = row[4], acc = row[5]))

        return models

    def _create_table(self):
        sql = "create table if not exists models (model_id INT auto_increment NOT NULL, model_name varchar(100) NOT NULL, dataset_name varchar(100) NOT NULL, mse FLOAT NOT NULL, auc_score FLOAT NOT NULL, accuracy FLOAT NOT NULL, model_path varchar(100) NOT NULL, CONSTRAINT NewTable_PK PRIMARY KEY (model_id))"
        
        self._dbh.execute(sql)
        self._db.commit()

    def add_model(self, model_name, dataset_name, mse, auc_score, accuracy, model_path):
        sql = "insert into models(model_name, dataset_name, mse, auc_score, accuracy, model_path) values('" +model_name +"', '" +dataset_name +"', " +str(mse) +", " +str(auc_score) +", " +str(accuracy) +", '" +model_path +"')"
        
        self._dbh.execute(sql)
        self._db.commit()
    
    def get_model_path_by_model_id(self, model_id):
        sql = "select model_path from models where model_id = " +str(model_id)
        
        self._dbh.execute(sql)
        record = self._dbh.fetchall()
        
        try:
            return record[0][0]
        except Exception as e:
            return None
    
    def get_all_model_paths(self):
        sql = "select model_path from models"
        
        self._dbh.execute(sql)
        return self._dbh.fetchall()
        

    def get_dataset_name_by_model_id(self, model_id):
        sql = "select dataset_name from models where model_id = " +str(model_id)

        self._dbh.execute(sql)
        record = self._dbh.fetchall()
        return record[0][0]
    
    def update_model_by_id(self, model_id, model_guid, model_name, mse, auc, acc):
        sql = "update models set model_name = '" +model_name +"', mse = " +str(mse) +", auc_score = " +str(auc) +", accuracy = " +str(acc) +", model_path = '" +os.path.join(model_guid, model_name) +"' where model_id = " +str(model_id)
        self._dbh.execute(sql)
        self._db.commit()
