import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import json
import logging

logging.basicConfig(format="%(levelname)s %(asctime)s %(message)s", level=logging.INFO)

logging.info("Reading csv file")
df = pd.read_csv("Processed_data.csv")
X = df.drop("Diabetes", axis=1)
Y = df["Diabetes"]
X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=0.3,random_state=0,stratify=Y)

logging.info("Scaling features")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.fit_transform(X_test)

logging.info("Training Model")
logreg = LogisticRegression()
logreg.fit(X_train_scaled, y_train)

logging.info("Predicting Model")
y_pred= logreg.predict(X_test_scaled)
y_test = y_test.values

logging.info("Calculating accuracy")
acc = np.mean(y_pred==y_test)
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
specificity = tn / (tn+fp)
sensitivity = tp / (tp + fn)
with open("metrics.json", 'w') as outfile:
    json.dump({ "accuracy": acc, "specificity": specificity, "sensitivity":sensitivity}, outfile)

logging.info("Saving confusion matrix figure")
cm = ConfusionMatrixDisplay.from_estimator(logreg,X_test_scaled,y_test)
cm.figure_.savefig('confusion_matrix.png')
