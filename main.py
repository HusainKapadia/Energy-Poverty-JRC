from flask import Flask, request, json #import main Flask class and request object
from forex_python.converter import CurrencyRates
from flask_cors import CORS
from datetime import timedelta
from datetime import datetime
import numpy as np
import pandas as pd


def read_data(household=1, typehh=0):
    if not typehh:
        data = pd.read_csv('useful_no_solar/run_household_{}/power2016Household.csv'.format(household), usecols=[2])
        data.columns = ['PowerConsumed']
        base = datetime(2016, 1, 1)
        dt = [base + timedelta(minutes=x) for x in range(len(data))]
        data['date'] = dt
        data = data.set_index('date')

        data = data.resample('D').mean()
        return data[-30:]
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
        data = data[data.index > datetime(2016, 6, 1)]
        data = data[data.index < datetime(2016, 7, 1)]

        data = data.resample('D').mean()
        return data[-30:]


app = Flask(__name__) #create the Flask app
CORS(app)

@app.route('/consumer_history')
def consumer_history():
    return read_data().to_json()

@app.route('/producer_history')
def producer_history():
    return read_data(typehh=1).to_json()

@app.route('/newsubmit', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        return json.dumps(['testing'])
    else:
        return "415 Unsupported Media Type ;)"
        
if __name__ == '__main_':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000
