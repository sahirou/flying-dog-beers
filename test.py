

# # package imports
# import dash
# import dash_bootstrap_components as dbc
# import dash_html_components as html
# import dash_core_components as dcc
# from dash.dependencies import Input, Output, State
# from dash import no_update
# from flask import session, copy_current_request_context

# import base64
# import os
# import pathlib
# from urllib.parse import quote as urlquote
# from flask import Flask, send_from_directory
# # import dash_table_experiments as dtab

# import dash
# from dash import Dash
# import dash_bootstrap_components as dbc
# import dash_core_components as dcc
# import dash_html_components as html
# import pandas as pd
# import numpy as np
# # import plotly.graph_objs as go
# import plotly.graph_objects as go
# from dash.dependencies import Input, Output, State
# import datetime as dt
# from datetime import datetime
# import pathlib
# from pathlib import Path
# import json
# # import dash_table
# import dash_auth
# import plotly.figure_factory as ff
# import plotly.express as px


import plotly.graph_objects as go
import dash
from dash import Dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import json


app = Dash()


#
fig = go.Figure()
fig.add_trace(go.Bar(
    y=['giraffes', 'orangutans', 'monkeys'],
    x=[20, 14, 23],
    name='SF Zoo',
    orientation='h',
    marker=dict(
        color='rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    )
))
fig.add_trace(go.Bar(
    y=['giraffes', 'orangutans', 'monkeys'],
    x=[12, 18, 29],
    name='LA Zoo',
    orientation='h',
    marker=dict(
        color='rgba(58, 71, 80, 0.6)',
        line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
    )
))

fig.update_layout(barmode='stack')



app.layout = html.Div([
    dcc.Graph(id="chart"),
    html.Br(),
    html.H1(id="zzz"),
    html.Pre(id='json_pre',style={'paddingTop':35})
])


@app.callback(
    Output('chart', 'figure')  ,
    [
        Input('zzz', 'children')
    ]
)
def generate_charte(zzz):
    return fig


@app.callback(
    Output('json_pre', 'children'),
    [
        Input('chart', 'clickData')
    ]
)
def debug_data(clickData):
    return json.dumps(clickData,indent=2)

if __name__ == "__main__":
    
    app.run_server(
        debug=True
    )