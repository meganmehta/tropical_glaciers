
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dbm
import plotly.graph_objs as go
import plotly.express as px 
import re
import pandas as pd

dry = pd.read_csv("/Users/meganmehta/Desktop/research/dry_glacier_output.csv")
wet = pd.read_csv("/Users/meganmehta/Desktop/research/wet_glacier_output.csv")

# Set up the app
app = dash.Dash(__name__)
server = app.server

#prelim data analysis - iqr v. median elevation
fig2 = px.scatter(dry, x="Median Elevation", y="Interquartile Range",
                 size="Area", color="Number of Cells filled for each glacier", hover_name="RGIId",
                 log_x=True, size_max=60)

#map with points displaying wet and dry glaciers (ADD WET GLACIERS)
fig = px.scatter_mapbox(dry, lat="CenLat", lon="CenLon", hover_name="RGIId", hover_data=["Zmed", "Area"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=1000)

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

#histogram of distribution of each individual glacier (have user select glacier from drop-down and populate)
fig3 = px.histogram(dry, x='Equilibrium Height')


#main components in HTML 
app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H1(children='glaciers in south america!'),

        html.Div(children='''
            predicting which glaciers are at the highest risk of disappearing
        '''),

        dcc.Graph(
        id='median_elevation_v_iqr',
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