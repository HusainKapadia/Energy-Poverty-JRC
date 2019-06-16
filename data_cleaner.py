'''
Extract useful information from provided data
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

solar_dir = './run_household_solar/*'
no_solar_dir = './runs_households_no_solar/*'

# Change the name for different directory
household_list = glob.glob(no_solar_dir)
# print(len(household_list))
for item in household_list:
    if 'cfg' in item:
        household_list.remove(item)


# Clean Grid Balance data
def clean_grid_bal(household_list):
    name = './gridbalance.2016'

    for dir in household_list:
        fname = f'{dir}/{name}'
        with open(fname, 'r') as f:
            grid_bal_data = f.read()

        grid_bal_list = grid_bal_data.splitlines()

        grid_bal_table = np.zeros([len(grid_bal_list), 5])
        for i, s in enumerate(grid_bal_list):
            grid_bal_table[i, :] = s.split()

        useful_grid_data = grid_bal_table[:, [0, 2, 3]]

        headers = ['Time', 'Power from grid', 'Power into grid']
        useful_grid_df = pd.DataFrame(useful_grid_data, columns=headers)

        sub_dir = dir.split("\\")[1]
        print(sub_dir)
        if not os.path.exists(f'./useful_solar/{sub_dir}'):
            os.makedirs(f'./useful_solar/{sub_dir}')

        save_csv = f'./useful_solar/{sub_dir}/gridbalance2016.csv'
        export_csv = useful_grid_df.to_csv(save_csv, header=True)

        # plt.figure()
        # plt.plot(useful_grid_data[:1441, 0], useful_grid_data[:1441, 2])

    # plt.show()

# Clean Household consumption Data
def clean_power_household(household_list, solar=True):
    name = './power.2016.Household.real'

    for dir in household_list:
        fname = f'{dir}/{name}'
        with open(fname, 'r') as f:
            power_data = f.read()

        power_list = power_data.splitlines()

        power_table = np.zeros([len(power_list), 8])
        for i, s in enumerate(power_list):
            power_table[i, :] = s.split()

        useful_power_data = power_table[:, [0, 1]]

        headers = ['Time', 'Power consumed']
        useful_power_df = pd.DataFrame(useful_power_data, columns=headers)

        sub_dir = dir.split("\\")[1]
        print(sub_dir)
        if solar:
            if not os.path.exists(f'./useful_solar/{sub_dir}'):
                os.makedirs(f'./useful_solar/{sub_dir}')
            save_csv = f'./useful_solar/{sub_dir}/power2016Household.csv'
        else:
            if not os.path.exists(f'./useful_no_solar/{sub_dir}'):
                os.makedirs(f'./useful_no_solar/{sub_dir}')
            save_csv = f'./useful_no_solar/{sub_dir}/power2016Household.csv'

        export_csv = useful_power_df.to_csv(save_csv, header=True)

        # plt.figure()
        # plt.plot(useful_power_data[:1441, 0], useful_power_data[:1441, 2])

    # plt.show()

# Extract solar module data
def clean_power_solarmod(household_list):
    name = './power.2016.Solar-Module.real'

    for dir in household_list:
        fname = f'{dir}/{name}'
        with open(fname, 'r') as f:
            power_data = f.read()

        power_list = power_data.splitlines()

        power_table = np.zeros([len(power_list), 9])
        for i, s in enumerate(power_list):
            power_table[i, :] = s.split()

        useful_power_data = power_table[:, [0, 1, 8]]

        headers = ['Time', 'Power consumed', 'Solar Power used']
        useful_power_df = pd.DataFrame(useful_power_data, columns=headers)

        sub_dir = dir.split("\\")[1]
        print(sub_dir)
        if not os.path.exists(f'./useful_solar/{sub_dir}'):
            os.makedirs(f'./useful_solar/{sub_dir}')

        save_csv = f'./useful_solar/{sub_dir}/power2016_solar_module.csv'
        export_csv = useful_power_df.to_csv(save_csv, header=True)

        # plt.figure()
        # plt.plot(useful_power_data[:1441, 0], useful_power_data[:1441, 1])
        # plt.plot(useful_power_data[:1441, 0], useful_power_data[:1441, 2])

    #plt.show()

# Extract info from yearly consumption file summary
def clean_consumption(household_list, solar=True):
    name = f'consumption.2016'

    for dir in household_list:
        fname = f'{dir}/{name}'
        print(fname)
        with open(fname, 'r') as f:
            consumption_data = f.read()

        splitted_list = consumption_data.split()
        print(splitted_list[8:15])
        try:
            households = splitted_list[8:15].index("1/1")
            print(households)
        except ValueError:
            households = splitted_list[8:15].index("1/2")
            print(households)

        sub_dir = dir.split("\\")[1]
        print(sub_dir)
        if solar:
            if not os.path.exists(f'./useful_solar/{sub_dir}'):
                os.makedirs(f'./useful_solar/{sub_dir}')
            with open(f'./useful_solar/{sub_dir}/num_people.txt', 'w') as f:
                f.write(str(households))
        else:
            if not os.path.exists(f'./useful_no_solar/{sub_dir}'):
                os.makedirs(f'./useful_no_solar/{sub_dir}')
            with open(f'./useful_no_solar/{sub_dir}/num_people.txt', 'w') as f:
                f.write(str(households))



clean_grid_bal(household_list)

# if solar = True, directly use household_list, if False, use household_list[1:], it still keeps 1 cfg.log file here
# Temporary fix for now
clean_power_household(household_list[1:], solar=False)

clean_consumption(household_list[1:], solar=False)

clean_power_solarmod(household_list)
