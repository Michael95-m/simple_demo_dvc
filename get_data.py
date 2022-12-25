import os
import logging

os.environ[
    "KAGGLE_USERNAME"
] = "<your-kaggle-username>"  ## change with your kaggle username from kaggle.json
os.environ[
    "KAGGLE_KEY"
] = "<your-kaggle-api-key>"  ## change with your api key file from kaggle.json
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile

logging.basicConfig(format="%(levelname)s %(asctime)s %(message)s", level=logging.INFO)

logging.info("Connecting kaggle api")
api = KaggleApi()
api.authenticate()
logging.info("Authentication Completed")

api.dataset_download_files("prosperchuks/health-dataset", path=".")
logging.info("Dataset Download Completed")

logging.info("Extracting Zip file")
with zipfile.ZipFile("health-dataset.zip", "r") as f:
    f.extractall("health_data")
logging.info("Extracting Done")
