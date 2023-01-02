import pandas as pd
from typing import Text
import yaml
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from utils.train import train
from utils.log import getlogger
import joblib
import argparse
import os

def data_train(config_path: Text) -> None:

    with open(config_path) as conf:
        conf = yaml.safe_load(conf)

    logger = getlogger("TRAIN MODEL")

    logger.info("Training set loaded")
    train_df = pd.read_csv(conf["data_split"]["trainset_path"])
    
    estimator = conf["train"]["estimator_name"]
    logger.info(f"Estimator name: {estimator}")

    target = conf["featurize"]["target_column"]
    param_grid = conf["train"]["estimators"][estimator]["param_grid"]
    cv = conf["train"]["cv"]

    y_train = train_df.loc[:, target].values.astype('int32')
    x_train = train_df.drop(target, axis=1)

    logger.info("Train model")
    model, scaler = train(x_train=x_train, y_train=y_train, estimator_name=estimator,
                        target=target, param_grid=param_grid,
                        cv=cv)
    logger.info(f"Best Score: {round(model.best_score_, 2)}")

    model_folder_path = conf["train"]["model_folder"]
    if not os.path.exists(model_folder_path):
        os.makedirs(model_folder_path)

    model_path = conf["train"]["model_path"]
    scaler_path = conf["train"]["scaler_path"]
    logger.info("Save model")
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)

if __name__ == "__main__":

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--config", dest="conf", required=True)
    args = args_parser.parse_args()

    data_train(args.conf)


    
    
    


