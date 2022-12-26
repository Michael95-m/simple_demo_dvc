# Simple demonstration about how to use dvc library
## 1. Project pipeline

### Downloading api key from kaggle

Since the data will be downloaded from kaggle, you first need to export your kaggle username and kaggle key as the environment variables like
```
export KAGGLE_USERNAME=*****
export KAGGLE_KEY=***** 
```
This must be done in your <b>command prompt</b>. 
If you don't know how to get KAGGLE_USERNAME and KAGGLE_KEY, you should probably read <b>Generating the API Key</b> section of [this article](https://insaid.medium.com/how-to-access-datasets-directly-from-kaggle-6a3552ea891c).


### Installation of dependencies
```
pip install -r requirements.txt
```
You can either install that either in your conda environment or in your python virtual environment. And I used python3.7 for this repository.

### Processing Pipeline

There are three steps needed to done by this project. First, download the data, process the data and train and evaluate the model.
All these three steps can be reproduced by using dvc by this command
```
dvc repro
``` 

In order to run this command, we need to prepare <b>dvc.yaml</b>. In this yaml file, all three stages named get_data, process_data and train are well defined by their cmd(command), deps(dependency), outs(output) and metrics(metric).