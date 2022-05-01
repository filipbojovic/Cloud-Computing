import mysql.connector
import config
from models.fastAPIModel import ModelAPI

class Db():
    __instance = None
    _db = None

    def __init__(self):
        self._db = mysql.connector.connect(user = config.user, password = config.password, host = config.host, database = config.db_name, port = config.port)
        self._create_table()
        Db.__instance = self

    @staticmethod
    def getInstance():
        if Db.__instance == None:
            Db()
        return Db.__instance
    
    def get_all_models(self):
        sql = "select * from models"
        dbh = self._db.cursor()
        dbh.execute(sql)
        records = dbh.fetchall()

        models = []
        for row in records:
            path = row[5]
            model_name = path.split('/')[1]
            models.append(ModelAPI(model_id = row[0], model_name = model_name, mse = row[2], auc = row[3], acc = row[4]))

        return models

    def _create_table(self):
        sql = "create table if not exists models (model_id INT auto_increment NOT NULL, model_name varchar(100) NOT NULL, mse FLOAT NOT NULL, auc_score FLOAT NOT NULL, accuracy FLOAT NOT NULL, model_path varchar(100) NOT NULL, CONSTRAINT NewTable_PK PRIMARY KEY (model_id))"
        dbh = self._db.cursor()
        dbh.execute(sql)
        self._db.commit()

    def add_model(self, model_name, mse, auc_score, accuracy, model_path):
        sql = "insert into models(model_name, mse, auc_score, accuracy, model_path) values('" +model_name +"', " +str(mse) +", " +str(auc_score) +", " +str(accuracy) +", '" +model_path +"')"
        dbh = self._db.cursor()
        dbh.execute(sql)
        self._db.commit()
    
    def get_model_path_by_model_id(self, model_id):
        sql = "select model_path from models where model_id = " +str(model_id)
        dbh = self._db.cursor()
        dbh.execute(sql)
        record = dbh.fetchall()
        
        return record[0][0]
