import pandas as pd
from typing import Text
import yaml
from utils.train import train
from utils.log import getlogger
import joblib
import argparse
import os


def data_train(config_path: Text) -> None:

    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    logger = getlogger("TRAIN MODEL", config["base"]["log_level"])

    logger.info("Training set loaded")
    train_df = pd.read_csv(config["data_split"]["trainset_path"])

    estimator = config["train"]["estimator_name"]
    logger.info(f"Estimator name: {estimator}")

    target = config["featurize"]["target_column"]
    param_grid = config["train"]["estimators"][estimator]["param_grid"]
    cv = config["train"]["cv"]

    y_train = train_df.loc[:, target].values.astype("int32")
    x_train = train_df.drop(target, axis=1)

    logger.info("Train model")
    model, scaler = train(
        x_train=x_train,
        y_train=y_train,
        estimator_name=estimator,
        param_grid=param_grid,
        cv=cv,
        random_state=config["base"]["random_state"],
    )
    logger.info(f"Best Score: {round(model.best_score_, 2)}")

    model_folder_path = config["train"]["model_folder"]
    if not os.path.exists(model_folder_path):
        os.makedirs(model_folder_path)

    model_path = config["train"]["model_path"]
    scaler_path = config["train"]["scaler_path"]
    logger.info("Save model")
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)


if __name__ == "__main__":

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--config", dest="conf", required=True)
    args = args_parser.parse_args()

    data_train(args.conf)
