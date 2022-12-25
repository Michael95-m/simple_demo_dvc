import pandas as pd
import numpy as np
import logging 

logging.basicConfig(format="%(levelname)s %(asctime)s %(message)s", level=logging.INFO)

logging.info("Reading csv file")
df = pd.read_csv("health_data/diabetes_data.csv")

logging.info("Dropping the features which are highly either unbalanced or unimportant")
df = df.drop(['CholCheck','Fruits','Veggies'],axis=1)
df.to_csv("Processed_data.csv", index=False)
logging.info("Wrote new file")


