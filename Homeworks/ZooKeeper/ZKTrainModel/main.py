import io
import config
import numpy as np
from http.client import HTTPException
import os
from filemanager import FileManager
import uvicorn
from database import Db
from models.ANNModel import ANN
import pandas as pd
from lib2to3.pytree import Base
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
import zipfile

app = FastAPI()
db = Db.getInstance()

@app.post("/trainMlModel") # dekorator
async def train_ml_model(optimizer: str = Form(...), batch_size: int = Form(...), num_of_epochs: int = Form(...), activation: str = File(...), output_activation: str = File(...), 
    num_of_outputs: int = File(...), dataset_name: str = File(...), dataset: UploadFile = File(...)):
    
    annModel = ANN(optimizer, batch_size, num_of_epochs, activation, output_activation, dataset_name)
    return annModel.train_model(dataset.file, num_of_outputs)

@app.get("/getAllModels")
async def get_all_models():
    return db.get_all_models()

@app.post("/predictValues")
async def predict_values(model_id: int = Form(...), num_of_outputs: int = Form(...), dataset: UploadFile = File(...)):

    path = db.get_model_path_by_model_id(model_id)

    if path == None:
        size = len(db.get_all_models())
        raise HTTPException(status_code = 404, detail = "Model not found. Currently exists " +str(size) +" models.")


    arr = ANN.predict(ANN.load_model(path), dataset.file, num_of_outputs)
    
    return {"predictions": arr[:, 0].tolist()}

@app.post("/updateModel")
async def update_model(model_id: int = Form(...), num_of_outputs: int = Form(...), new_model: UploadFile = File(...)):

    old_model_path = db.get_model_path_by_model_id(model_id) # GUID + model_name

    if old_model_path == None:
        raise HTTPException(status_code = 404, detail = "Model not found.")

    new_model_guid, new_model_name = FileManager.replace_model(new_model, old_model_path)

    # if new_model_guid == False:
    #     raise HTTPException(status_code = 409, detail = "Model already exists.")

    dataset_name = db.get_dataset_name_by_model_id(model_id)

    mse, acc, auc = ANN.evaluate_existing_model(model_path = os.path.join(new_model_guid, new_model_name), dataset = FileManager.read_dataset(dataset_name), num_of_outputs = num_of_outputs)
    db.update_model_by_id(model_id, new_model_guid, new_model_name, mse = mse, auc = auc, acc = acc)

    zipped_file_name = "zipped.zip"

    paths = list()
    paths.append(os.path.join(config.storage_path, new_model_guid, new_model_name))

    zipFilePath = os.path.join(zipped_file_name)
    FileManager.zipit(paths, zipFilePath)

    body = {}
    body["guid"] = new_model_guid
    body["old_model_name"] = old_model_path.split("/")[1]


    def iterfile():
        with open(zipFilePath, mode = "rb") as file_like:
            yield from file_like
    return StreamingResponse(iterfile(), media_type = "application/octet-stream", headers = body)
    

@app.get("/downloadAllModels")
async def download_all_models():
    paths = db.get_all_model_paths()
    paths = np.array(paths)
    paths = paths[:, 0]
    for i in range(len(paths)):
        paths[i] = os.path.join(config.storage_path, paths[i].split("/")[0])

    zipped_file_name = "zipped.zip"
    zip_file_path = os.path.join(zipped_file_name)
    FileManager.zipit(paths.tolist(), zip_file_path)

    
    # return StreamingResponse(io.BytesIO(), media_type = "application/zip")

    def iterfile():
        with open(zip_file_path, mode = "rb") as file_like:
            yield from file_like
    return StreamingResponse(iterfile(), media_type = "application/octet-stream")
    
