import zipfile
from typing import Text
import yaml
import argparse
import json
import os
from utils.log import getlogger

def read_kaggle_json():
    with open("kaggle.json") as f:
        kaggle_data = json.load(f)

        return kaggle_data 

def get_data(config_path: Text) -> None:
    
    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    logger = getlogger("GET_DATA", config["base"]["log_level"])

    logger.info("Connect with Kaggle api")
    api = KaggleApi()
    api.authenticate()
    logger.info("Download data from kaggle")
    api.dataset_download_files("prosperchuks/health-dataset", path="./")
    with zipfile.ZipFile(config["data_load"]["dataset_zip"], "r") as f:
        f.extractall(config["data_load"]["dataset_folder"])
    logger.info("Save the data")

if __name__ == "__main__":

    kaggle_data = read_kaggle_json()
    os.environ["KAGGLE_USERNAME"] = kaggle_data["username"]
    os.environ["KAGGLE_KEY"] = kaggle_data["key"]
    from kaggle.api.kaggle_api_extended import KaggleApi

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--config", dest="config", required=True)
    args = args_parser.parse_args()

    get_data(config_path=args.config)



