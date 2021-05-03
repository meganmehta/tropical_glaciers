
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dbm
import plotly.graph_objs as go
import plotly.express as px 
import re
import pandas as pd
import os 


#version Python 3.7.2
current_dir = os.getcwd() #expected output = 'Users/*your username*
#if you changed output file from data_modifications.py, make sure to change it here too!
file_extension = "/Desktop/tropical_glaciers/data/data_modifications_output.csv"
filepath = current_dir + file_extension
allData = pd.read_csv(filepath)

dry = allData.loc[allData['Glacier Type'] == "Dry"]
wet = allData.loc[allData['Glacier Type'] == "Wet"]

# Set up the app
app = dash.Dash(__name__)
server = app.server

#IQR v. Median Elevation - add drop down for wet v. dry v. all
#fig2 = px.scatter(allData, x = "Median Elevation", y = "Interquartile Range",
                 #size = "Area", color = "Number of Cells filled for each glacier", hover_name="RGIId",
                 #log_x = True, size_max=60)

fig2 = go.Figure()

for glacierType in ['Wet', 'Dry']:
    df = allData[allData["Glacier Type"] == glacierType]
    fig2.add_trace(go.Scatter(x=allData["Median Elevation"], y=allData["Interquartile Range"], line={}, name=glacierType))




#Map with wet and dry glaciers - add drop down for wet v. dry v. all 
fig = px.scatter_mapbox(allData, lat="CenLat", lon="CenLon", hover_name="RGIId", hover_data=["Zmed", "Area"],
                        color_discrete_sequence=["blue"], zoom=3, height=1000)

fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])

#main components in HTML 
app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H1(children='glaciers in south america!'),

        html.Div(children='''
            predicting which glaciers are at the highest risk of disappearing
        '''),

        dcc.Graph(
        id ='median_elevation_v_iqr',
        figure=fig2
    ), 
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='select glacier types'),

        html.Div(children='''
            overview of wet or dry glaciers
        '''),

        dcc.Dropdown(
        options=[
            {'label': 'Wet Glaciers', 'value': 'wet'},
            {'label': 'Dry Glaciers', 'value': 'dry'}
        ],
        value=['wet', 'dry'],
        multi=True
    ),
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='overview of glaciers'),

        html.Div(children='''
            overview of wet and dry glaciers
        '''),

        dcc.Graph(
        id='glacier Coverage',
        figure=fig
    ), 
    ]),
    
])


if __name__ == "__main__":
    app.run_server(debug=True)