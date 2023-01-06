import pandas as pd
import argparse
from typing import Text
import yaml
import joblib
from utils.evaluate import (
    get_report,
    get_confusion_matrix,
    get_plot,
    get_translated_result,
)
import json
import os
from utils.log import getlogger


def model_evaluate(config_path: Text) -> None:
    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    logger = getlogger("MODEL EVALUATE", config["base"]["log_level"])

    logger.info("Testset loaded")
    test = pd.read_csv(config["data_split"]["testset_path"])
    target = config["featurize"]["target_column"]
    y_test = test.loc[:, target].values.astype(int)
    x_test = test.drop(target, axis=1)

    logger.info("Model loaded")
    model_path = config["train"]["model_path"]
    scaler_path = config["train"]["scaler_path"]
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    logger.info("Predict test set")
    x_test_scaled = scaler.transform(x_test)
    y_pred = model.predict(x_test_scaled)

    logger.info("Calculate the accuracy")
    cm = get_confusion_matrix(y_pred, y_test)
    report = get_report(cm)
    report_folder = config["evaluate"]["report_folder"]
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    logger.info("Save accuracy report")
    accuracy_report_path = config["evaluate"]["accuracy_report_path"]
    with open(accuracy_report_path, "w") as json_file:
        json.dump(report, json_file, indent=4)
    logger.info(f"Save the report at: {accuracy_report_path}")

    logger.info("Save translated result to plot")
    cm_df = get_translated_result(y_pred, y_test)
    cm_df.to_csv(config["evaluate"]["translated_report_path"], index=False)

    logger.info("Save Confusion Matrix")
    confusion_matrix_path = config["evaluate"]["confusion_matrix_path"]
    target_names = config["evaluate"]["target_names"]
    plot = get_plot(cm, target_names)
    plot.savefig(confusion_matrix_path)
    logger.info(f"Save the confusion matrix at: {confusion_matrix_path}")


if __name__ == "__main__":

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--config", dest="conf", required=True)
    args = args_parser.parse_args()

    model_evaluate(args.conf)
