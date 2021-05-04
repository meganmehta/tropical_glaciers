#%%
import matplotlib.pyplot as plt 
from scipy import stats
import pandas as pd 
import csv 
import numpy as np
import plotly.express as px
import os 

#version Python 3.7.2
current_dir = os.getcwd() #expected output = 'Users/*your username*
#if you changed output file from data_modifications.py, make sure to change it here too!
file_extension = "/Desktop/tropical_glaciers/data/data_modifications_output.csv"
filepath = current_dir + file_extension
allData = pd.read_csv(filepath)

zmid_vals = allData[allData.columns[11:85]].to_numpy() #dataset with just the area values at each zmid point
area_vals = allData['Area'].to_numpy() #only area values of each glacier 
zmed_val = allData['Zmed'].to_numpy() #only zmed values for each glacier 

zmid_values = allData.columns[11:85].astype(int).to_numpy() #list of all zmid value points 

glacier_value = "RGI60-" + str(input("Enter the glacier RGIId that you want to view: "))
print("Glacier ID: ", glacier_value)

corresponding_val = 0
row_count = 0
for i in range(0, len(allData)):
    row_count += 1
    if glacier_value == allData.iloc[i]['RGIId']:
        corresponding_val = row_count - 1

selected_glacier_area = area_vals[corresponding_val]
print("Area of glacier:", selected_glacier_area)
selected_zmed = zmed_val[corresponding_val]
print("Zmed of glacier:", selected_zmed)
matching_row = zmid_vals[corresponding_val]

input_AAR = float(input("Enter the accumulation area ratio: "))
print("AAR: ", input_AAR)

matching_row_area = []
for item_area in matching_row:
    #item_area = item_ratio * selected_glacier_area.astype(int)
    matching_row_area.append(item_area)

matching_row_a = np.array(matching_row)
zmid_values = zmid_values.astype(float)
calculated_equilibrium = np.interp(1-input_AAR, (matching_row_a.cumsum()/selected_glacier_area), zmid_values) 

print("Calculated equilibrium elevation: ", calculated_equilibrium)

#creates dictionary used in algorithm 
plot_data = dict(zip(zmid_values, matching_row_a))

updated_plot_data = {x:y for x,y in plot_data.items() if y!=0}
last_key = list(updated_plot_data.keys())[-1]
first_key = list(updated_plot_data.keys())[0]
print("Highest elevation point with recorded area:", last_key)

true_ELA_val = float(input("Enter the true ELA value for the glacier you selected: "))
print("True ELA value: ", true_ELA_val)

new_area = selected_glacier_area

#initial conditions for algorithm 
if true_ELA_val > last_key - 50:
        print("Glacier is going to melt for sure. There will be a large area loss.")
elif true_ELA_val < calculated_equilibrium:
        print("Glacier is growing overtime. No net loss.")

algorithm = pd.DataFrame.from_dict(updated_plot_data, orient='index').T
range_of_glacier = list(updated_plot_data.keys())

#maybe include new calculated equilibrium and new area for each run through 
#percent of starting area, and add new area in dataframe 
while true_ELA_val > 0 and calculated_equilibrium > 0:
    if true_ELA_val > calculated_equilibrium and true_ELA_val < last_key - 50:
        if len(updated_plot_data) > 1:
            updated_plot_data.pop(first_key)
            first_key = list(updated_plot_data.keys())[0]
            dict_keys = np.asarray(list(updated_plot_data.keys()))
            row_vals = np.asarray(list(updated_plot_data.values()))
            new_area = row_vals.sum()
            calculated_equilibrium = np.interp(1-input_AAR, (row_vals.cumsum()/new_area), dict_keys)
            algorithm = algorithm.append(pd.DataFrame.from_dict(updated_plot_data, orient='index').T)
            print("New calculated equilibrium is:", calculated_equilibrium)
    else:
        area_loss = selected_glacier_area - new_area
        print("Committed area loss:", area_loss, "km^2")
        percent_loss = (area_loss/selected_glacier_area) * 100
        print("Percent loss: ", percent_loss, "%")
        print("End")
        break
 
algorithm.fillna(0)
algorithm = algorithm.T
algorithm['count'] = algorithm.reset_index().index
algo_iterations = algorithm['count'].to_list()
fig = px.scatter(algorithm.T, x=range_of_glacier, y=algorithm.columns, animation_frame=algo_iterations, animation_group=algorithm.columns, 
range_y=[0,2])
fig.show()
# %%
