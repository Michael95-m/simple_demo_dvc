import pandas as pd
from typing import Text
import yaml
import os
from utils.log import getlogger
import argparse


def feature_select(config_path: Text) -> None:
    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    logger = getlogger("FEATURE_SELECT", config["base"]["log_level"])
    logger.info("Read raw data")
    df = pd.read_csv(config["data_load"]["dataset_csv"])
    if not os.path.exists(config["featurize"]["feature_folder"]):
        os.makedirs(config["featurize"]["feature_folder"])

    logger.info("Dropping unimportant feature")
    df = df.drop(config["featurize"]["drop_features"], axis=1)

    logger.info("Save Feature selected csv")
    df.to_csv(config["featurize"]["features_path"], index=False)


if __name__ == "__main__":

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--config", dest="config", required=True)
    args = args_parser.parse_args()

    feature_select(args.config)
