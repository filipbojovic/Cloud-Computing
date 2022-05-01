import uvicorn
from database import Db
from models.ANNModel import ANN
import pandas as pd
from lib2to3.pytree import Base
from fastapi import FastAPI, File, UploadFile, Form

app = FastAPI()
db = Db.getInstance()

@app.post("/trainMlModel") # dekorator
async def train_ml_model(optimizer: str = Form(...), batch_size: int = Form(...), num_of_epochs: int = Form(...), activation: str = File(...), output_activation: str = File(...), 
    num_of_outputs: int = File(...), model_name: str = File(...), dataset: UploadFile = File(...)):
    
    annModel = ANN(optimizer, batch_size, num_of_epochs, activation, output_activation, model_name)
    return annModel.train_model(dataset.file, num_of_outputs)

@app.get("/getAllModels")
async def get_all_models():
    return db.get_all_models()

@app.post("/predictValues")
async def predict_values(model_id: int = Form(...), num_of_outputs: int = Form(...), dataset: UploadFile = File(...)):

    path = db.get_model_path_by_model_id(model_id)
    arr = ANN.predict(ANN.load_model(path), dataset.file, num_of_outputs)
    
    return {"predictions": arr[:, 0].tolist()}
