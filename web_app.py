
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dbm
import plotly.graph_objs as go
import plotly.graph_objects as px
import plotly.express as px 
import numpy as np
import re
import pandas as pd
import os 

#run in Python 3.7.2
current_dir = os.getcwd() #expected output = 'Users/*your username*
#if you changed output file from data_modifications.py, make sure to change it here too!
file_extension = "/Desktop/tropical_glaciers/data/data_modifications_output.csv"
filepath = current_dir + file_extension
allData = pd.read_csv(filepath)

dry = allData.loc[allData['Glacier Type'] == "Dry"]
wet = allData.loc[allData['Glacier Type'] == "Wet"]

zmid_values = allData.columns[11:85]

#Dash App Setup 
app = dash.Dash(__name__)
server = app.server

#Map with all glacier data
fig = px.scatter_mapbox(allData, lat="CenLat", lon="CenLon", hover_name="RGIId", hover_data=["Zmed", "Area"],
                        color="Glacier Type", zoom=7, height=500, color_discrete_sequence=['red', 'blue'],)

fig.update_layout(
    title="Map of All Glaciers",
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
    ]
)

#IQR v. Median Elevation 
#area = thousandths place, round elevations + IQR  to whole number 
fig2 = go.Figure(data=[
    go.Scatter(
        name="Dry Glaciers", 
        x=dry["Median Elevation"], 
        y=dry["Interquartile Range"], 
        mode="markers",
        marker=dict(
            size=60,
            color=dry["Number of Cells filled for each glacier"], #set color equal to a variable
            colorscale='Sunset', 
            showscale=True
        ),
        text=dry["RGIId"],
        hovertemplate=
        "Glacier ID: %{text}<br>" + 
        "Median Elevation: %{x}<br>" +
        "Interquartile Range: %{y}<br>" +
        "Range of Glacier Area: %{marker.size}" +
        "<extra></extra>",
        marker_size=dry["Number of Cells filled for each glacier"] * 4,
        
    ), 
    go.Scatter(
        name="Wet Glaciers", 
        x=wet["Median Elevation"],
        y=dry["Interquartile Range"],
        mode="markers",
        marker=dict(
            size=16,
            color=wet["Number of Cells filled for each glacier"], 
            colorscale='Viridis',
            showscale=True
        ),
        text=wet["RGIId"],
        hovertemplate=
        "Glacier ID: %{text}<br>" + 
        "Median Elevation: %{x}<br>" +
        "Interquartile Range: %{y}<br>" +
        "Range of Glacier Area: %{marker.size}" +
        "<extra></extra>",
        marker_size=dry["Number of Cells filled for each glacier"] * 4,
    ), 
    go.Scatter(
        name="Dry and Wet Glaciers",
        x=allData["Median Elevation"],
        y=allData["Interquartile Range"],
        mode="markers",
        marker=dict(
            size=16,
            color=allData["Number of Cells filled for each glacier"],
            colorscale='Portland', 
            showscale=True, 
        ),
        text=allData["RGIId"],
        hovertemplate=
        "Glacier ID: %{text}<br>" + 
        "Median Elevation: %{x}<br>" +
        "Interquartile Range: %{y}<br>" +
        "Range of Glacier Area: %{marker.size}" +
        "<extra></extra>",
        marker_size=allData["Number of Cells filled for each glacier"] * 4,
    )
])

fig2.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(label="Wet and Dry", 
                    method="update", 
                    args=[{"visible":[False, False, True]},
                    {"title":"IQR v. Median Elevation for Wet and Dry Glaciers"}]),
                dict(label="Wet", 
                    method="update", 
                    args=[{"visible":[False, True, False]},
                    {"title":"IQR v. Median Elevation for Wet Glaciers"}]),
                dict(label="Dry", 
                    method="update", 
                    args=[{"visible":[True, False, False]},
                    {"title":"IQR v. Median Elevation for Dry Glaciers"}]),
            ])
        )
    ],
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Open Sans"
    ),
    title="IQR v. Median Elevation",
    xaxis_title="Median Elevation",
    yaxis_title="Interquartile Range",
    font=dict(
        family="Open Sans, sans-serif",
        size=14,
        color="Black"
    ),
)

#Individual Glacier Histograms (to see area distribution)
glacier_ids = allData['RGIId'].unique()

#main components in HTML 
app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H1(children='Glaciers in south america!', style={'color': 'Black', 'fontSize': 50, 'fontFamily':'Open Sans'}),

        html.Div(children='''
            overview of wet and dry glaciers 

        '''),

        dcc.Graph(
        id='glacier Coverage',
        figure=fig
        ),

        html.Div(children='''
            An independent study on glaciers in south america
        '''),

        dcc.Graph(
            id ='median_elevation_v_iqr',
            figure=fig2
        ), 

        dcc.Graph(
            id="single_glacier_area_distribution",
        ),

        dcc.Dropdown(
            id='glacier-id-selector',
            options=[{'label': i, 'value':i} for i in glacier_ids],
            value='16.00010'
        )

    ]),  
])

@app.callback(
    Output('single_glacier_area_distribution', 'figure'),
    Input('glacier-id-selector', 'value'),
)

#print table, print total area and do percents + median elevation
def update_graph(selected_glacier_id):
    glacier_id_data = allData[allData['RGIId'] == selected_glacier_id]
    zmid_values = glacier_id_data.columns[11:85].to_list()
    filtered_data = glacier_id_data[glacier_id_data.columns[11:85]]
    figure = px.bar(glacier_id_data, x=zmid_values, y=filtered_data.T)
    return figure

if __name__ == "__main__":
    app.run_server(debug=True)