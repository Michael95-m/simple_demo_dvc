import pandas as pd
import yaml
from typing import Text
from utils.log import getlogger
from sklearn.model_selection import train_test_split
import argparse

def data_split(config_path: Text) -> None:

    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    logger = getlogger("DATA_SPLIT")

    df = pd.read_csv(config["featurize"]["features_path"])
    logger.info("Split the data")
    train, test = train_test_split(df, test_size=config["data_split"]["test_size"], random_state=config["base"]["random_state"])
    logger.info("Save train and test sets")
    train.to_csv(config["data_split"]["trainset_path"])
    test.to_csv(config["data_split"]["testset_path"])

if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--config", dest="conf", required=True)
    args = args_parser.parse_args()

    data_split(args.conf)

    