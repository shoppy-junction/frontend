# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import colorlover as cl

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# df = pd.read_csv('processed_output.csv')
df = pd.read_csv('test_data_processed.csv')

scl = cl.scales['9']['seq']['Blues']
colorscale = [ [ float(i)/float(len(scl)-1), scl[i] ] for i in range(len(scl)) ]

# x_range = df2['SepalWidth'].min()
# y_range = df2['SepalWidth'].min()

app.layout = html.Div(children=[
    html.H1(children='Shoppy Insights',style={'textAlign': 'center'}),

    # dcc.Graph(
    #     id='location-graoh',
    #     figure={
    #         'data': [
    #             go.Scatter(
    #                 x=df['x'],
    #                 y=df['y'],
    #                 # text='User: {}'.format(df['userid']),
    #                 text=df['userid'],
    #                 mode='markers',
    #                 opacity=0.7,
    #                 # name=df['userid'],
    #                 # marker={
    #                 #     'size': 15,
    #                 #     'line': {'width': 0.5, 'color': 'white'}
    #                 # },
    #             )
    #         ],
    #         'layout': go.Layout(
    #             # xaxis={'type': 'log', 'title': 'GDP Per Capita'},
    #             # yaxis={'title': 'Life Expectancy'},
    #             # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
    #             # legend={'x': 0, 'y': 1},
    #             hovermode='closest'
    #         )
    #     }
    # ),
    dcc.Graph(
        id='density-graph',
        figure={
            'data': [
                go.Histogram2dContour(
                    x=df['x'],
                    y=df['y'],
                    name='density',
                    # mode='markers',
                    ncontours=20,
                    colorscale=colorscale,
                    # showscale=False
                ),
                go.Scatter(
                    x=df['x'],
                    y=df['y'],
                    name='density',
                    mode='markers',
                    # ncontours=20,
                    # colorscale=colorscale,
                    # showscale=False
                )
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
                showlegend=False,
                autosize=False,
                width=700,
                height=700,
                hovermode='closest',
                bargap=0,

                # showticklabels
                xaxis=dict(range=[0,20],domain=[0, 1], linewidth=2, linecolor='#444',
                           showgrid=False, zeroline=False, ticks='', showticklabels=True, showline=True, mirror=True),

                yaxis=dict(range=[0,23],domain=[0, 1],linewidth=2,linecolor='#444',
                           showgrid=False, zeroline=False, ticks='', showticklabels=True, showline=True, mirror=True),
                xaxis2=dict(range=[0,20],domain=[0, 1], linewidth=2, linecolor='#444',
                           showgrid=False, zeroline=False, ticks='', showticklabels=True, showline=True, mirror=True),

                yaxis2=dict(range=[0,23],domain=[0, 1],linewidth=2,linecolor='#444',
                           showgrid=False, zeroline=False, ticks='', showticklabels=True, showline=True, mirror=True),
            )
        }
    ),
    # dcc.Graph(
    #     id='scatter-graph',
    #     figure={
    #         'data': [
    #             go.Scatter(
    #                 x=df['x'],
    #                 y=df['y'],
    #                 name='density',
    #                 mode='markers',
    #                 # ncontours=20,
    #                 # colorscale=colorscale,
    #                 # showscale=False
    #             ),
    #         ],
    #         'layout': go.Layout(
    #             images= [dict(
    #                 source= 'assets/store_with_grid.jpg',
    #                 xref= "paper",
    #                 yref= "paper",
    #                 x= 0,
    #                 y= 1,
    #                 sizex= 1,
    #                 sizey= 1,
    #                 sizing= "stretch",
    #                 opacity= 0.5,
    #                 layer= "above")],
    #             showlegend=False,
    #             autosize=False,
    #             width=700,
    #             height=700,
    #             hovermode='closest',
    #             bargap=0,

    #             # showticklabels
    #             xaxis=dict(range=[0,20],domain=[0, 1], linewidth=2, linecolor='#444',
    #                        showgrid=False, zeroline=False, ticks='', showticklabels=True, showline=True, mirror=True),

    # yaxis=dict(range=[0,23],domain=[0, 1],linewidth=2,linecolor='#444',
    #                        showgrid=False, zeroline=False, ticks='', showticklabels=True, showline=True, mirror=True),
    # xaxis2=dict(range=[0,20], domain=[0, 1], showgrid=False, zeroline=False, ticks='',
    #             showticklabels=False ),

    # yaxis2=dict(range=[0,23], domain=[0, 1], showgrid=False, zeroline=False, ticks='',
    #             showticklabels=False ),
    #         )
    #     }
    # )
])

if __name__ == '__main__':
    app.run_server(debug=True)
