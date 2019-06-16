from flask import Flask, request, json #import main Flask class and request object
from forex_python.converter import CurrencyRates
from flask_cors import CORS
from datetime import timedelta
from datetime import datetime
import os.path as osp
import numpy as np
import pandas as pd
import glob


def all_productionf():
    # Read all folders and load the power consumption of all households into one frame
    dfs = []
    for p in glob.glob('useful_solar/*'):
        grid_balance = pd.read_csv(osp.join(p, 'gridbalance2016.csv'), usecols=[0, 3], index_col=0)
        solar_module = pd.read_csv(osp.join(p, 'power2016_solar_module.csv'), usecols=[0, 3], index_col=0)
        production = grid_balance['Power into grid'] + solar_module['Solar Power used']
        dfs.append(production.to_frame())

    dfs = pd.concat(dfs, axis=1)
    dfs.columns = ['production_h' + p.split('_')[-1] for p in glob.glob('useful_solar/*')]
    dt = [datetime(2016, 1, 1)]
    for _ in range(len(dfs)-1): 
        dt.append(dt[-1] + timedelta(seconds=60))

    dfs['Date'] = dt
    dfs.set_index('Date', drop=True, inplace=True)
    overall_production = dfs.sum(axis=1)
    overall_production = overall_production.to_frame()
    overall_production.columns = ['OverallProd']
    return overall_production


def all_consumptionf(): 
    # Households Total comsumption
    base_solar = osp.join('useful_solar')
    household_list = glob.glob(f'{base_solar}/*')
    consumption = [0] * 527040
    for item in household_list:
        household = osp.join(item, 'power2016Household.csv')
        householddata = pd.read_csv(household)
        #print(householddata['Power consumed'][:1000])
        consumption = consumption + householddata['Power consumed'][:]

    base_no_solar = osp.join('useful_no_solar')
    household_list2 = glob.glob(f'{base_no_solar}/*')
    for item in household_list2:
        if 'cfg' in item:
            household_list2.remove(item)

    for item in household_list:
        household = osp.join(item, 'power2016Household.csv')
        householddata = pd.read_csv(household)
        #print(householddata['Power consumed'][:1000])
        consumption = consumption + householddata['Power consumed'][:]


    dt = [datetime(2016, 1, 1)]
    for _ in range(len(consumption)-1): 
        dt.append(dt[-1] + timedelta(seconds=60))

    total = consumption.to_frame()
    total['date'] = dt

    total.set_index('date', drop=True, inplace=True)
    total.columns = ['Power consumed']

    return total

def forecast():
    t = datetime.now()
    prod = all_production[(all_production.index > t) & (all_production.index < t + timedelta(hours=24))]
    cons = all_consumption[(all_consumption.index > t) & (all_consumption.index < t + timedelta(hours=24))]
    surplus = pd.DataFrame(prod.values - cons.values)
    surplus.index = cons.index
    surplus.columns = ['Surplus']
    surplus = surplus.resample('H').mean()
    surplus.index = list(range(len(surplus)))
    return surplus

def read_data(household=1, typehh=0):
    if not typehh:
        data = pd.read_csv('useful_no_solar/run_household_{}/power2016Household.csv'.format(household), usecols=[2])
        data.columns = ['PowerConsumed']
    else:
        data = pd.read_csv('useful_solar/run_household_solar_{}/power2016Household.csv'.format(household), usecols=[2])
        sol = pd.read_csv('useful_solar/run_household_solar_{}/power2016_solar_module.csv'.format(1), usecols=[3])
        hh = pd.read_csv('useful_solar/run_household_solar_{}/gridbalance2016.csv'.format(1), usecols=[3])
        data.columns = ['PowerConsumed']
        data['Produced'] = sol.values + hh.values
    base = datetime(2016, 1, 1)
    dt = [base + timedelta(minutes=x) for x in range(len(data))]
    data['date'] = dt
    data = data.set_index('date')
    t = datetime.now()
    data.index = data.index + timedelta(days=(3*365) + 1) # Shift values 3 years
    data = data[data.index < t]
    data = data.resample('D').mean()
    return data[-7:]

# Readjust times
all_production = all_productionf()
all_consumption = all_consumptionf()
all_production.index = all_production.index + timedelta(days=(3*365) + 1)
all_consumption.index = all_consumption.index + timedelta(days=(3*365) + 1)

app = Flask(__name__) #create the Flask app
CORS(app)

@app.route('/consumer_history')
def consumer_history():
    return read_data().to_json()

@app.route('/producer_history')
def producer_history():
    return read_data(typehh=1).to_json()


@app.route('/forecast')
def forecast_newdata():
    return forecast().to_json()

@app.route('/newsubmit', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        return json.dumps(['testing'])
    else:
        return "415 Unsupported Media Type ;)"
        
if __name__ == '__main_':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000
