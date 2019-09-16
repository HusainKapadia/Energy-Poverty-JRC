from datetime import timedelta, datetime
import time
from flask import jsonify #import main Flask class and request object
import os.path as osp
import numpy as np
import pandas as pd
import glob
import random
import pandas as pd
from datetime import datetime
from datetime import timedelta
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor

prosumers = ['London Webster', 'Quincy Brooks', 'Jazmine Barry', 'Megan Knight', 'Journey Dyer', 'Jazmin Glover', 'Alison Zimmerman', 'Tommy Hale', 'Kobe Fields', 'Jamison Davila', 'Areli James', 'Celeste Russo', 'Kaleb Cole', 'Braden Woodward', 'Rene Bradshaw', 'Brycen Mcknight', 'Alexandria Wood', 'Kaylyn Harper', 'Ean Mullins', 'Cindy Yu']
consumersp = [random.randint(2, 8) for _ in range(20)]

def infer_monthly_usage():
    # Load dataset
    fulldata = pd.read_pickle('prod/weather_prod_cons.pkl')
    n_prosumers = 20
    X = fulldata.copy().dropna()
    y_prod = X.OverallProd
    y_cons = X.Consumption
    X = X.drop(columns=['OverallProd', 'Consumption'])

    # Prepare Data, Train XgBoost Regressor and Fit model
    xtrain, xtest, ytrain, ytest = train_test_split(X, y_prod, shuffle=False)
    reg_prod = XGBRegressor()
    reg_prod.fit(xtrain.values, ytrain)
    prod_preds = pd.Series(reg_prod.predict(fulldata.drop(columns=['OverallProd', 'Consumption']).values), index=fulldata.index)

    xtrain, xtest, ytrain, ytest = train_test_split(X, y_cons, shuffle=False)
    reg_cons = XGBRegressor()
    reg_cons.fit(xtrain.values, ytrain)
    cons_preds = pd.Series(reg_cons.predict(fulldata.drop(columns=['OverallProd', 'Consumption']).values), index=fulldata.index)

    # Resample to give prediction per month
    res = pd.DataFrame({'Production': prod_preds.resample('M', how='sum'), 
                        'Consumption': cons_preds.resample('M', how='sum')}).sort_index() 
    res['Deficit'] = res.Consumption - res.Production
    res['ProsumersNeeded'] =  round(res.Deficit/(res.Production/n_prosumers)).astype(int)
    res['Coverage'] =  round((res.Production*100)/res.Consumption).astype(int)
    res.index = res.index.month_name()
    res = res[['ProsumersNeeded', 'Coverage']]
    return res


def read_data(household=1, typehh=0):
    if not typehh:
        data = pd.read_csv('useful_no_solar/run_household_{}/power2016Household.csv'.format(household), usecols=[2])
        data.columns = ['PowerConsumed']
    else:
        data = pd.read_csv('useful_solar/run_household_solar_{}/power2016Household.csv'.format(household), usecols=[2])
        sol = pd.read_csv('useful_solar/run_household_solar_{}/power2016_solar_module.csv'.format(household), usecols=[3])
        hh = pd.read_csv('useful_solar/run_household_solar_{}/gridbalance2016.csv'.format(household), usecols=[3])
        data.columns = ['PowerConsumed']
        data['Produced'] = sol.values + hh.values
    base = datetime(2016, 1, 1)
    dt = [base + timedelta(minutes=x) for x in range(len(data))]
    data['date'] = dt
    data = data.set_index('date')
    t = datetime.now()
    data.index = data.index + timedelta(days=(3*365) + 1) # Shift values 3 years
    data = data[data.index < t]
    data = data.resample('D').sum()/100
    return data

res = infer_monthly_usage().T.to_dict()