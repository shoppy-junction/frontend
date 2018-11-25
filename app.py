# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from datetime import datetime
# import colorlover as cl

external_stylesheets = ['https://fonts.googleapis.com/css?family=Catamaran', 'https://fonts.googleapis.com/css?family=Fredoka One']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Shoppy Insights'

# df = pd.read_csv('processed_output.csv')
# df = pd.read_csv('../backend/data/location_data_processed.csv')
df = pd.read_csv('../backend/data/noisy_location_processed.csv')
df2 = pd.read_csv('../backend/data/purchase_data_processed.csv')

min_time = min(df["timestamp"].min(), df2["timestamp"].min())
max_time = max(df["timestamp"].max(), df2["timestamp"].max())

moneys = df2.groupby(['x','y'])
moneys_points = list(moneys.groups.keys())
# df2 = pd.read_csv('fake_purchase_data.csv')
# df = pd.read_csv('test_data_processed_swampped.csv')

# scl = cl.scales['9']['seq']['Blues']
# colorscale = [ [ float(i)/float(len(scl)-1), scl[i] ] for i in range(len(scl)) ]

# x_range = df2['SepalWidth'].min()
# y_range = df2['SepalWidth'].min()

time_data = {309: 'Front', 342: 'Center aisles', 430: 'Back'}
money_data = {60: 'Front', 26: 'Center aisles', 17: 'Back'}

app.layout = html.Div(children=[
    html.H1(children='Shoppy Insights',style={'textAlign': 'center'}),

    html.H5(
        '',
        id='time_range_text',
        style={'text-align': 'right'}
    ),

    dcc.RangeSlider(
        id='time_slider',
        # count=1,
        # step=1,
        min=min_time,
        max=max_time,
        value=[min_time, max_time]
    ),

    # html.Div(
    # [
    #         html.H5(
    #             '',
    #             id='well_text',
    #             className='two columns'
    #         ),
    #         html.H5(
    #             '',
    #             id='production_text',
    #             className='eight columns',
    #             style={'text-align': 'center'}
    #         ),
    #         html.H5(
    #             '',
    #             id='year_text',
    #             className='two columns',
    #             style={'text-align': 'right'}
    #         ),
    #     ],
    dcc.Graph(
        id='money-graph',
    ),
    dcc.Graph(
        id='noisy-graph',
    ),
    dcc.Graph(
        id='telia-graph',
    ),
    dcc.Dropdown(
        id='telia-dropdown',
        options=[
            {'label': 'Sunday', 'value': 'sun'},
            {'label': 'Monday', 'value': 'mon'},
            {'label': 'Tuesday', 'value': 'tue'},
            {'label': 'Wednesday', 'value': 'wed'}
        ],
        value='sun'
    ),
    dcc.Graph(
        id='time-chart',
        figure={
            'data': [
                go.Pie(labels=list(time_data.values()), values=list(time_data.keys()))
                ],
            'layout':go.Layout(
            title='Time spent per region',
            )
            }    
    ),
    dcc.Graph(
        id='money-chart',
        figure={
            'data': [
                go.Pie(labels=list(money_data.values()), values=list(money_data.keys()))
                ],
            'layout':go.Layout(
            title='Money spent per region',
            )
       }
    )
])

# Slider -> time text
@app.callback(Output('time_range_text', 'children'),
              [Input('time_slider', 'value')])
def update_time_text(time_slider):
    return "{} - {}".format(datetime.fromtimestamp(time_slider[0]).strftime('%H:%M:%S'), datetime.fromtimestamp(time_slider[1]).strftime('%H:%M:%S on %a, %b %d'))

# Slider -> Green graph
@app.callback(
    dash.dependencies.Output('money-graph', 'figure'),
    [dash.dependencies.Input('time_slider', 'value')])
def update_money_figure(time_slider):
    var1 = df2['timestamp'] >= time_slider[0]
    var2 = df2['timestamp'] <= time_slider[1]
    filtered_df2 = df2[var1 & var2].reset_index()

    moneys = filtered_df2.groupby(['x','y'])
    moneys_points = list(moneys.groups.keys())

    return {
        'data': [
            go.Histogram2dContour(
                x=[p[0] for p in moneys_points],
                y=[p[1] for p in moneys_points],
                z=[sum(moneys.get_group(p)['price']) for p in moneys_points],
                name='density',
                # mode='markers',
                    ncontours=40,
                colorscale='Greens',
                reversescale=True,
                # showscale=False
                ),
            ],
        'layout': go.Layout(
            images= [dict(
                source= 'assets/store_with_grid.jpg',
                xref= "paper",
                yref= "paper",
                x= 0,
                y= 1,
                sizex= 1,
                sizey= 1,
                sizing= "stretch",
                opacity= 0.5,
                layer= "above")],
            title="Shopper Activity",
            showlegend=False,
            autosize=False,
            width=800,
            height=800,
            hovermode='closest',
            bargap=0,

                # showticklabels
                xaxis=dict(range=[0,20], linewidth=2, linecolor='#444',
                           showgrid=False, zeroline=False, ticks='', showticklabels=False, showline=True, mirror=True),

                yaxis=dict(range=[0,23],linewidth=2,linecolor='#444',
                           showgrid=False, zeroline=False, ticks='', showticklabels=False, showline=True, mirror=True),
        )
    }

# Slider -> Red graph
@app.callback(
    dash.dependencies.Output('noisy-graph', 'figure'),
    [dash.dependencies.Input('time_slider', 'value')])
def update_noisy_figure(time_slider):
    var1 = df['timestamp'] >= time_slider[0]
    var2 = df['timestamp'] <= time_slider[1]
    filtered_df = df[var1 & var2].reset_index()
    return {
        'data': [
            go.Histogram2dContour(
                x=filtered_df['x'],
                y=filtered_df['y'],
                name='density',
                # mode='markers',
                ncontours=40,
                colorscale='Hot',
                reversescale=True,
                # showscale=False
                ),
            ],
        'layout': go.Layout(
            images= [dict(
                source= 'assets/store_with_grid.jpg',
                xref= "paper",
                yref= "paper",
                x= 0,
                y= 1,
                sizex= 1,
                sizey= 1,
                sizing= "stretch",
                opacity= 0.5,
                layer= "above")],
            title="Shopper Activity",
            showlegend=False,
            autosize=False,
            width=800,
            height=800,
            hovermode='closest',
            bargap=0,

                # showticklabels
                xaxis=dict(range=[0,20], linewidth=2, linecolor='#444',
                           showgrid=False, zeroline=False, ticks='', showticklabels=False, showline=True, mirror=True),

                yaxis=dict(range=[0,23],linewidth=2,linecolor='#444',
                           showgrid=False, zeroline=False, ticks='', showticklabels=False, showline=True, mirror=True),
        )
    }

@app.callback(
    dash.dependencies.Output('telia-graph', 'figure'),
    [dash.dependencies.Input('telia-dropdown', 'value')])
def update_figure(selected_day):
    df_telia = pd.read_csv('../backend/data/telia_activity.txt')
    df_telia = df_telia[df_telia.dominant_zone == 212]
    if selected_day == 'sun':
        df_filtered = df_telia[df_telia.time.str.startswith('21.1.2018')]
    elif selected_day == 'mon':
        df_filtered = df_telia[df_telia.time.str.startswith('22.1.2018')]
    elif selected_day == 'tue':
        df_filtered = df_telia[df_telia.time.str.startswith('23.1.2018')]
    elif selected_day == 'wed':
        df_filtered = df_telia[df_telia.time.str.startswith('24.1.2018')]
    else:
        print(selected_day)
        df_filtered = df_telia #[df_telia.time.str.startswith('21.1.2018') | df_telia.time.str.startswith('22.1.2018') | df_telia.time.str.startswith('23.1.2018') | df_telia.time.str.startswith('24.1.2018')| df_telia.time.str.startswith('25.1.2018')| df_telia.time.str.startswith('26.1.2018') | df_telia.time.str.startswith('27.1.2018')]
    def hour(ts):
        return int(ts.time[-8:-6])
    df_filtered['hour'] = df_filtered.apply(hour, axis=1)
    df_sorted = df_filtered.sort_values(by='hour')
    return {
            'data': [
                go.Bar(
                    x=df_sorted['hour'],
                    y=df_sorted['count']/500
                    ),
            ],
            'layout': go.Layout(
                title="Longitudinal Store Activity",
                autosize=False,
                width=800,
                height=800
            )
        }

if __name__ == '__main__':
    app.run_server(debug=True)
