#%%
import matplotlib.pyplot as plt 
from scipy import stats
import pandas as pd 
import csv 
import numpy as np
import plotly.express as px

#trying to merge files together 
dry = pd.read_csv("/Users/meganmehta/Desktop/research/Dry_Region_RGI_Data_Complete.csv")
wet = pd.read_csv("/Users/meganmehta/Desktop/research/Wet_Region_RGI_Data_Complete.csv")
np.set_printoptions(threshold=np.inf)

dry["Glacier Type"] = "dry"
wet["Glacier Type"] = "wet"

glaciers = [dry, wet]
allData = pd.concat(glaciers)


zmid_vals = allData[allData.columns[10:]].to_numpy() #dataset with just the area values at each zmid point
area_vals = allData['Area'].to_numpy() #only area values of each glacier 
zmed_val = allData['Zmed'].to_numpy() #only zmed values for each glacier 

zmid_values = allData.columns[10:].astype(int).to_numpy() #list of all zmid value points 

glacier_value = "RGI60-" + input("Enter the glacier RGIId that you want to view: ")
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
for item_ratio in matching_row:
    item_area = item_ratio * selected_glacier_area
    matching_row_area.append(item_area)

matching_row_a = np.asarray(matching_row_area)
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

#actual for loop running through 
while true_ELA_val > 0 and calculated_equilibrium > 0:
    if true_ELA_val > calculated_equilibrium and true_ELA_val < last_key - 50:
        if len(updated_plot_data) > 1:
            updated_plot_data.pop(first_key)
            first_key = list(updated_plot_data.keys())[0]
            dict_keys = np.asarray(list(updated_plot_data.keys()))
            row_vals = np.asarray(list(updated_plot_data.values()))
            new_area = row_vals.sum()
            calculated_equilibrium = np.interp(1-input_AAR, (row_vals.cumsum()/new_area), dict_keys)
            print("New calculated equilibrium is:", calculated_equilibrium)
    else:
        print("Committed area loss:", selected_glacier_area - new_area)
        print("End")
        break

# %%
