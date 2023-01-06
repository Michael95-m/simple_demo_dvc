from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
import pandas as pd
from typing import Dict, Text
from sklearn.metrics import make_scorer, f1_score
import numpy as np

class UnsupportedClassifier(Exception):
    
    def __init__(self, estimator_name):
        self.msg = f"Unsupported classifier name {estimator_name}"
        super.__init__(self.msg)

def get_supported_estimator() -> Dict:
    return {
        "logreg": LogisticRegression,
        "knn":  KNeighborsClassifier,
        "xgb":  XGBClassifier,
        "dectree":  DecisionTreeClassifier,
        "randforest":   RandomForestClassifier 
    }

def train(x_train: pd.DataFrame, y_train: np.ndarray, estimator_name: Text, param_grid: Dict, cv: int, random_state: int):

    estimators = get_supported_estimator()

    if estimator_name not in estimators.keys():
        raise UnsupportedClassifier(estimator_name)

    if estimator_name == "dectree" or estimator_name == "randforest": ## to get reproducibility, need to see random_state
        estimator = estimators[estimator_name](random_state=random_state) 
    else:
        estimator = estimators[estimator_name]()

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    scorer = make_scorer(f1_score, average='weighted')
    clf=GridSearchCV(estimator=estimator,
                    param_grid=param_grid,
                    cv=cv,
                    verbose=1,
                    scoring=scorer)
    clf.fit(x_train_scaled, y_train)

    return clf, scaler


    

    

    


