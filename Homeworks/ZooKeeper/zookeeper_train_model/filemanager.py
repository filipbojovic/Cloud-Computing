import pandas as pd
import config
import zipfile
import os
import shutil
import io

class FileManager:
    def replace_model(zipped_model, old_model_full_path):

        old_model_guid = old_model_full_path.split("/")[0]

        with zipfile.ZipFile(io.BytesIO(zipped_model.file.read()), 'r') as zip_ref:
            zip_ref.extractall(os.path.join(config.storage_path, old_model_guid))

        """ find new model names"""
        new_model_name = zipped_model.filename
        new_model_name = new_model_name.removesuffix(".zip")
        # new_model_name = os.listdir(os.path.join(config.storage_path))[0]
        
        """ remove old model """
        try:
            shutil.rmtree(os.path.join(config.storage_path, old_model_full_path))
        except Exception as e:
            print("Model '", old_model_full_path, "' does not exists.")

        return old_model_guid, new_model_name
        
    
    def read_dataset(dataset_name):
        return pd.read_csv(os.path.join(config.datasets_path, dataset_name +".csv"))
    
    def zipit(folders, zip_location):

        try:
            os.remove(zip_location)
        except Exception as e:
            print("There is no garbage .zip file.")

        zip_file = zipfile.ZipFile(zip_location, 'w', zipfile.ZIP_DEFLATED)

        for folder in folders:
            for dirpath, dirnames, filenames in os.walk(folder):
                for filename in filenames:
                    zip_file.write(
                        os.path.join(dirpath, filename),
                        os.path.relpath(os.path.join(dirpath, filename), os.path.join(folders[0], '../')))

        zip_file.close()
