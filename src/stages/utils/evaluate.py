import numpy as np
from sklearn.metrics import confusion_matrix
from typing import Dict, List
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

def get_confusion_matrix(y_pred: np.ndarray, y_test: np.ndarray) -> np.ndarray:

    cm = confusion_matrix(y_test, y_pred)

    return cm

def get_report(cm: np.ndarray) -> Dict:
    
    tn, fp, fn, tp = cm.ravel()
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    specificity = tn / (tn+fp)
    sensitivity = tp / (tp + fn)
    report = {"accuracy": round(accuracy, 2),
            "specificity": round(specificity, 2),
            "sensitivity": round(sensitivity, 2)}

    return report

def get_plot(cm: np.ndarray, target_names: List):

    cm_df = pd.DataFrame(cm, index=target_names, columns=target_names)

    plt.figure(figsize=(5,4))
    sns.heatmap(cm_df, annot=True, cmap='Blues', fmt='d')
    plt.title('Confusion Matrix')
    plt.ylabel('Actal Values')
    plt.xlabel('Predicted Values')
    plt.show()

    return plt.gcf()



