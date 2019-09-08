import pandas as pd
from datetime import datetime
from datetime import timedelta
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor

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
    res.index = res.index.month_name()
    return res
