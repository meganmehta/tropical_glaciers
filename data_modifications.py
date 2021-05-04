import pandas as pd 
import csv 
import numpy as np 
import os 
#import geopy
#from geopy.geocoders import Nominatim
#from geopy.extra.rate_limiter import RateLimiter

#run in Python 3.7.2
#figure out dynamic filepaths 
current_dir = os.getcwd() #expected output should be /Users/*your username*

#clone the folder in your local Desktop
dry_extension = "/Desktop/tropical_glaciers/data/Dry_Region_RGI_Data_Complete.csv"
wet_extension = "/Desktop/tropical_glaciers/data/Wet_Region_RGI_Data_Complete.csv"

dry_filepath = current_dir + dry_extension
wet_filepath = current_dir + wet_extension

dry = pd.read_csv(dry_filepath)
wet = pd.read_csv(wet_filepath)

dry["Glacier Type"] = "Dry"
wet["Glacier Type"] = "Wet"

glaciers = [dry, wet]

#combine both RGI datasets
allData = pd.concat(glaciers)

#used to print out complete dataset in terminal 
np.set_printoptions(threshold=np.inf)

zmid_values = allData[allData.columns[10:85]]
allData_matrix = zmid_values.to_numpy()

zmid_numbers = allData.columns[10:85].astype(int).to_numpy()
allData_areas = allData['Area'].to_numpy()

#calculates mean elevation at each zmid point 
total_areas = []
for row in allData_matrix:
    zmid_num = 3025
    means = []
    for number in row:
        mean_elevation = number * zmid_num
        means.append(mean_elevation)
        if zmid_num < 6775:
            zmid_num+=50
        else:
            break
    total_areas.append(means)

#glaciers with acutal area value instead of ratio
glacier_area_vals = pd.DataFrame(total_areas, columns=zmid_numbers)
#columns 1-10 on allData
glacier_info = allData[allData.columns[0:10]]
glacier_types = allData[allData.columns[85]]
#revised allData that includes the actual area value at every elevation point 
allData = pd.concat([glacier_info, glacier_area_vals, glacier_types], axis=1, join='inner')

total_mean_elevation = []
for glacier in total_areas:
    mean_sum = 0
    for elevation in glacier:
        mean_sum+=elevation
    total_mean_elevation.append(mean_sum)
allData['Mean Elevations'] = total_mean_elevation

#creating new variables for every glacier 
row_count = 0
allData_median_elevation = []
allData_interquartile_range = []
allData_filled_cells = []
allData_max_point = []
allData_min_point = []
for row in allData_matrix:
    mean_sum = 0
    row = np.array(row)
    row_no_zero = np.trim_zeros(row)
    zipped_rows = np.array(list(zip(zmid_numbers,row)))
    filled_cells = 0
    median_elevation = np.interp(0.5, row.cumsum(), zmid_numbers)
    interquartile_range = np.interp(0.75, row.cumsum(), zmid_numbers) - np.interp(0.25, row.cumsum(), zmid_numbers)
    max_point = np.argmax(row)
    max_elevation = zmid_numbers[max_point]
    min_point = np.amin(row_no_zero)
    for item in zipped_rows:
        if item[1] == min_point:
            min_elevation = item[0]
    for item in row:
        if item > 0:
            filled_cells+=1
    #number of rows should be 1464
    if row_count < 1464:
        row_count+=1
    else:
        break

    allData_median_elevation.append(median_elevation)
    allData_interquartile_range.append(interquartile_range)
    allData_filled_cells.append(filled_cells)
    allData_max_point.append(max_elevation)
    allData_min_point.append(min_elevation)

allData['Median Elevation'] = allData_median_elevation
allData['Interquartile Range'] = allData_interquartile_range
allData['Number of Cells filled for each glacier'] = allData_filled_cells
allData['Height with greatest area'] = allData_max_point
allData['Height with lowest area'] = allData_min_point


#change output file to whatever name you choose!
endFile_extension = "/Desktop/tropical_glaciers/data/data_modifications_output.csv"
end_filepath = current_dir + endFile_extension
allData.to_csv(end_filepath)
print("Done")
