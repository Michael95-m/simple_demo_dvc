# Simple demonstration about how to use dvc library
## 1. Requirements

### 1.1 Downloading api key from kaggle

Since the data will be downloaded from kaggle, you first need to export your kaggle username and kaggle key as the environment variables like
```
export KAGGLE_USERNAME=*****
export KAGGLE_KEY=***** 
```
This must be done in your <b>command prompt</b>. 
If you don't know how to get KAGGLE_USERNAME and KAGGLE_KEY, you should probably read <b>Generating the API Key</b> section of [this article](https://insaid.medium.com/how-to-access-datasets-directly-from-kaggle-6a3552ea891c).

If you don't want to type your KAGGLE_USERNAME and KAGGLE_KEY everytime, there is another method. You could make a shell script (let's assume your_script.sh) and write the following in your script like
```
#!/bin/sh

export KAGGLE_USERNAME=******
export KAGGLE_KEY=*******
```

Then Run this command in your command prompt like
```
. your_script.sh
```

This approach can have the same effect as the first approach. You don't need to type **export** command everytime and just run the shell script as like that.

Note `export` command will work only for **linux** machines. If you use **window** machine, use `SET` instead of `export` (SET is equivalent of export in window). And also second method will not work in **window** machines. Honestly, I don't know how to write shell script equivalent in window OS.

### 1.2. Installation of dependencies
```
pip install -r requirements.txt
```
You can either install that either in your conda environment or in your python virtual environment. And I used python3.7 for this repository.

If you run in your python virtual environment, then add virtual environment to Jupyter Notebook
```
python -m ipykernel install --user --name=dvc-venv
```

## 2. Processing Pipeline

There are five steps needed to done by this project. First, download the data, select the features,split the data, train the model and evaluate it.
All these five steps can be reproduced by using dvc by this command
```
dvc repro
``` 

In order to run this command, we need to prepare <b>dvc.yaml</b>. In this yaml file, all five stages named data_get, feature_select, data_split, train and evaluate are well defined by their `cmd`(command), `deps`(dependency), `params`(parameter), `outs`(output),`metrics`(metric) and `plots`(plot).

`dvc repro` is useful for automation of the pipeline. It is also useful for reproducibility of the data pipeline.

## 3. Visualizing metrics and plots

### 3.1. Visualizing metrics

It is vital to have reproducible pipelines so that we can easily manage experiments. We also need to evaluate  experiments by their resulting metrics such as accuracy. That's why metrics are a requirement for experiment management.

When dvc is used, we can add structured metrics  as an output of our reproducible pipeline and can also visualize the metrics. 

To track the metrics, we need to add `metrics` parameter in the stage (evaluate stage in demo) of dvc.yaml. We also need to give `cache: false` to that. Then we can track the experiment result by using 

```sh
dvc metrics show
```

Another useful command is `dvc metrics diff`. This command shows the difference between the experiments. In order to work properly with this command, you need to track the **log file** associated with accuracy (**report/report.json** in my demo) with **git**. If that log file is ignored by git, you will get the blank value in `head` column.

### 3.2 Visualizing Plots

In most of the cases, visualizing only metrics is not enough. We also need to visualize the plots too. 

In my demo, the pipeline can generate the confusion matrix by using **seaborn** library. But there is another way we can generate this by using dvc. In order to do that, we just need a csv which consists of two columns (predicted value and true value for target column) with their respective value. Then the command that can generate the plot is 

```sh
## template format is for confusion matrix and x-axis is the column named y_pred for predicted value and y-axis is y_test for true value which are from the file named confusion_matrix_data.csv inside report.
dvc plots show report/confusion_matrix_data.csv --template confusion -x y_pred -y y_test 
```

## 4. CI (Continous Integration)

For CI, ci.yaml is created inside `.github/workflows` folder. You can write certain commands from **cml** library to output your model result  to readme file and also can check the error inside your pipeline.