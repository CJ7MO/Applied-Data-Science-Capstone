# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# dropdown values
launch_sites = spacex_df['Launch Site'].unique().tolist()
sites = []
sites.append({'label': 'All Sites', 'value': 'All Sites'})
for site in launch_sites:
    sites.append({'label': site, 'value': site})

# marks values for slider
marks = {i: str(i) for i in range(int(min_payload), int(max_payload+1001), 1000)}

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(
                                    id='site_dropdown',
                                    options=sites,
                                    placeholder='Select a Launch Site',
                                    search_value=True,
                                    value='All Sites'),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                dcc.RangeSlider(id='payload-slider',
                                                min=min_payload,
                                                max=10000,
                                                step=1000,
                                                marks=marks,
                                                value=[0, 10000]),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback([Output(component_id='success-pie-chart', component_property='figure'),
               Output(component_id='success-payload-scatter-chart', component_property='figure')],
              [Input(component_id='site_dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def graph_compute(dropdown, slider):
    if dropdown == 'All Sites':
        df = spacex_df[spacex_df['class'] == 1]
        pie_chart = px.pie(df, names='Launch Site', hole=.3, title='Total Success Launches by All Sites')
    else:
        df = spacex_df.loc[spacex_df['Launch Site'] == dropdown]
        pie_chart = px.pie(df, names='class', hole=.3, title='Total Success Launches by' + str(dropdown))
    if dropdown == 'All Sites':
        min_payload, max_payload = slider
        df = spacex_df
        mask = (df['Payload Mass (kg)'] > min_payload) & (df['Payload Mass (kg)'] < max_payload)
        scatter_plot = px.scatter(
            df[mask],
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version',
            size='Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'])
    else:
        min_payload, max_payload = slider
        df = spacex_df.loc[spacex_df['Launch Site'] == dropdown]
        mask = (df['Payload Mass (kg)'] > min_payload) & (df['Payload Mass (kg)'] < max_payload)
        scatter_plot = px.scatter(
            df[mask],
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version',
            size='Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'])
    return pie_chart, scatter_plot


# Run the app
if __name__ == '__main__':
    app.run_server(port="1717")
