from datetime import timedelta, datetime
import time
import os.path as osp
import numpy as np
import pandas as pd
import glob
import random

prosumers = ['London Webster', 'Quincy Brooks', 'Jazmine Barry', 'Megan Knight', 'Journey Dyer', 'Jazmin Glover', 'Alison Zimmerman', 'Tommy Hale', 'Kobe Fields', 'Jamison Davila', 'Areli James', 'Celeste Russo', 'Kaleb Cole', 'Braden Woodward', 'Rene Bradshaw', 'Brycen Mcknight', 'Alexandria Wood', 'Kaylyn Harper', 'Ean Mullins', 'Cindy Yu']
consumersp = [random.randint(2, 8) for _ in range(20)]

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

def read_all_prosumers():
    for i in range(1, 21):
        print('Reading producer {}/20'.format(i))
        p = read_data(household=i, typehh=0)
        p.to_csv('consumer_data/consumer{}.csv'.format(i))

read_all_prosumers()