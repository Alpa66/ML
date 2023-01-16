import numpy as np
import mlflow
import pandas as pd
import datetime
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.seasonal import seasonal_decompose
import sys


mlflow.set_experiment(experiment_name='STL')
df = pd.read_csv('./realTraffic/speed_t4013.csv', parse_dates=['timestamp'])
df.index = df.timestamp
df.drop(columns=['timestamp'], inplace=True)
res = STL(df, seasonal=7, period=12).fit()
deviation = np.array(res.resid.abs())
most_likely_outlier = deviation.max()
Thresholds = np.linspace(0, most_likely_outlier, 5)
params = {'th': Thresholds}
num = (-1, -1)
with mlflow.start_run(run_name="PARENT_RUN"):
    for th in params['th']:
        with mlflow.start_run(run_name="CHILD_RUN", nested=True):
            mlflow.log_param(key='threshold', value=th)
            outliers_ind = np.where(res.resid.abs() > th)
            outlier_values = df.iloc[outliers_ind]
            temp = float(len(outlier_values))
            percentage = temp / len(df)
            mlflow.log_metric(key='NO. Anomalies', value=temp)
            mlflow.log_metric(key='Percentage of anomalies', value=percentage)
            if num == (-1, -1):
                num = (len(outlier_values), th)
            else:
                if len(outlier_values) > 0:
                    if temp < num[0]:
                        num = (int(temp), th)
                    if percentage < (1.0 / 1000.0):
                        break
print(num)
print('Volume is working just fine!')
