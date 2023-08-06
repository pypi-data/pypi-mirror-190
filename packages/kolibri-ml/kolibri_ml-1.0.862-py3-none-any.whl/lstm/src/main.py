import logging

import pandas as pd

from lstm.src.lstm_predictor import FPA

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


import os

if __name__ == "__main__":

    model_config = {
        "columns_to_drop": [],
        "group_by_columns": ['Period_Start_Date', 'Employee_Id', 'Employee_Status', 'Variable_Id'],
        "group_column": "Employee_Id",
        "date_column": "Original_Start_Date",
        "features": ["Employee_Status"],
        "epochs": 4,
        "target": 35,
        "dummies": ["Employee_Status"],
        "normalize_columns": [],
        "horizon": 1,
        "min_window": 1,
        "max_window": 3,
        "pre-train": True,
        "train": True,
        "n_jobs": -1,
        "container-name": "lstmmodel",
        "set": ["val"],
        "remote-storage": "",#"azure-blob",
        "multi_variate_output": False,
        "output-folder": "/Users/mohamedmentis/Dropbox/Mac (2)/Documents/Mentis/Development/Python/kolibri-ml/lstm/outputs"
    }
    os.environ[
        'AZURE_STORAGE_CONNECTION_STRING'] = "DefaultEndpointsProtocol=https;AccountName=mentis1;AccountKey=8LHRahnNg+uIPiJVMsdxKZlILKYrmcPnwJ+ZYZiizI4EkDBmDrCU38ZTQwbNSkvxeQidIBnH+SpEmq0vq+s0pw==;EndpointSuffix=core.windows.net"

    train_data=pd.read_csv("/Users/mohamedmentis/Dropbox/Mac (2)/Documents/Mentis/Development/Python/kolibri-ml/lstm/notebooks/Test_data_5_weeks.csv")#.sample(5000)

    current_data= pd.read_csv("/Users/mohamedmentis/Dropbox/Mac (2)/Documents/Mentis/Development/Python/kolibri-ml/lstm/notebooks/Test_data_5_weeks.csv")

    fpa=FPA(train_data, model_config)
    print(fpa.train())
    model=fpa.load_model()
    res=fpa.detect(current_data)

    print(res)


