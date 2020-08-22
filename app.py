"""
Dash App

"""
import base64
import os
import pathlib
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
# import dash_table_experiments as dtab

import dash
from dash import Dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
# import plotly.graph_objs as go
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import datetime as dt
from datetime import datetime
import pathlib
from pathlib import Path
# import json
# import dash_table
import dash_auth
from controls import overview_layout

mapbox_access_token = 'pk.eyJ1Ijoic2FuaXJvdSIsImEiOiJja2U0cWwweDEwdnlhMnpsZm9oeWJzNm84In0.Xwoh5FQDOPwq-vUWFqzEcA'

# Get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
UPLOAD_DIRECTORY = PATH.joinpath("app_uploaded_files").resolve()

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# init export file
Path(os.path.join(UPLOAD_DIRECTORY, "extract.csv"),exist_ok=True).touch()

# Load data
df = pd.read_csv(DATA_PATH.joinpath("upsales_app.csv"),sep=";") #low_memory=False)
df["DATE"] = pd.to_datetime(df["DATE"])
zoning = df[['DACR','ZONE','SECTEUR']].drop_duplicates(keep='first')
filtered_data = pd.DataFrame()
#
date_sup =  pd.to_datetime(str(max(df['DATE']))).strftime('%Y-%m-%d')
date_inf =  pd.to_datetime(str(min(df['DATE']))).strftime('%Y-%m-%d')
current_date = date_sup


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'upsales': '123@range'
}

server = Flask(__name__)
app = Dash(server=server,external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.title = "Capillarité"

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


# load data


# DACR Dropdown options
DACRS = list(zoning['DACR'].unique())
dacr_options = [
    {"label": dacr, "value": dacr} for dacr in DACRS
]

# Zone Dropdown options
ZONES = list(zoning['ZONE'].unique())
zone_options = [
    {"label": zone, "value": zone} for zone in ZONES
]


# Sector Dropdown options
SECTEURS = list(zoning['SECTEUR'].unique())
secteur_options = [
    {"label": secteur, "value": secteur} for secteur in SECTEURS
]

# POS activity Dropdown options
ACTIVITIES = [
    'Orange Money'
]
activity_options = [
    {"label": activity, "value": activity} for activity in ACTIVITIES
]

# POS global stutus options
STATUS = [
    'Actif',
    'Future inactif',
    'Inactif récent',
    'Inactif âgé'
]
status_options = [
    {"label": status, "value": status} for status in STATUS
]

# POS cx status options
OM_CX_CATEGORIES = [
    'Performant',
    'Presque performant',
    'Non performant'
]
om_cx_category_options = [
    {"label": category, "value": category} for category in OM_CX_CATEGORIES
]


# Colors
COLORS = {
    'foucha' : '#ff00ff'
}

# Status COlors
markers_colors = {
    'Actif': 'green',
    'Future inactif': 'blue',
    'Inactif récent': 'orange',
    'Inactif âgé': 'red'
}


table_style = {
	'align-items': 'center',
	'border-radius': '5px',
	'background-color': 'white',
	'margin': '0.5rem',
	'padding': '1rem',
	'position': 'relative',
	'border': '1px solid #f1f1f1',
    'height': '500px',
	'overflow': 'scroll'
}

# Logo
logo = html.Div(
    [
        html.Img(
            src=app.get_asset_url("orange_logo.png"),
            id="logo_orange",
            style={
                "height": "60px",
                "width": "auto",
                "margin-bottom": "25px",
            }
        )
    ],
    className="dash-bootstrap",
    style={"float":"right"}
)

# Control form
controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Date",style={'margin-right':'0.5rem','marging-top' : '3rem'}),
                html.Br(),
                dcc.DatePickerSingle(
                    id='date_selector',
                    min_date_allowed=date_inf,
                    max_date_allowed=date_sup,
                    initial_visible_month=current_date,
                    date=current_date,
                    display_format="DD/MM/YYYY",
                    className="dash-bootstrap"
                ),
            ]
        ),
        # Activités, Status, Rupture
        dbc.FormGroup(
            [
                html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(153,153,153)'}),
                dbc.Label("Activités"),
                dcc.Dropdown(
                    id="pos_activity_selector",
                    options=activity_options,
                    placeholder="Select POS activities",
                    disabled=True,
                    multi=True,
                    value=[ACTIVITIES[0]],
                ),
            ]
        ),
        dbc.FormGroup(
            [
                html.Br(),
                dbc.Label("Statut global"),
                dbc.Checklist(
                    options=status_options,
                    value=STATUS,
                    id="global_om_status_selector",
                    switch=True,
                    inline=True
                ),
            ]
        ),
        dbc.FormGroup(
            [
                html.Br(),
                # html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(153,153,153)'}),
                dbc.Label("Statut Cash in/Cash out"),
                dbc.Checklist(
                    options=status_options,
                    value=STATUS,
                    id="cashx_status_selector",
                    switch=True,
                    inline=True
                ),
            ]
        ),
        dbc.FormGroup(
            [
                html.Br(),
                # html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(135,153,153)'}),
                dbc.Label("Rupture de stock"),
                dbc.Checklist(
                    options=[{'label': 'Oui', 'value': 'Oui'},{'label': 'Non', 'value': 'Non'}],
                    value=['Oui','Non'],
                    id="oos_status_selector",
                    # switch=True,
                    inline=True
                ),
            ]
        ),
        # Filtres Géo
        dbc.FormGroup(
            [
                html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(153,153,153)'}),
                # html.P('Filtres Géo',style={'margin-top':'0','text-align': 'right','font-style': 'italic','color':'red'}),
                dbc.Label("Régions"),
                dcc.Dropdown(
                    id="dacr_selector",
                    placeholder="Select DACR(S)...",
                    options=dacr_options,
                    multi=True,
                    value=['Niamey','Dosso','Tillaberi']
                ),
            ]
        ),
        html.Br(),
        dbc.FormGroup(
            [
                dbc.Label("Zones"),
                dcc.Dropdown(
                    id="zone_selector",
                    placeholder="Select ZONE(S)...",
                    options=zone_options,
                    multi=True,
                    value=ZONES,
                ),
            ]
        ),
        html.Br(),
        dbc.FormGroup(
            [
                dbc.Label("Secteurs"),
                dcc.Dropdown(
                    id="sector_selector",
                    placeholder="Select SECTOR(S)...",
                    options=secteur_options,
                    multi=True,
                    value=SECTEURS,
                ),
            ]
        ),
        # Submit
        dbc.FormGroup(
            [
                html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(135,153,153)'}),
                dbc.Button("Valider", id="submit_button", className="mr-2",style={'display': 'inline-block','float':'right'}),
                # html.Span(id="example-output", style={"vertical-align": "middle"}),
            ]
        ),
    ],
    body=True,
)

# Visu
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Overview", className="card-text"),
            # dbc.Button("Click here", color="success"),
            overview_layout,
        ],
        id="visu_overview"
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            # html.P("Map", className="card-text"),
            dcc.Graph(id="mapbox_fig"),
            # dbc.Button("Click here", color="success"),
        ],
        id="visu_map"
    ),
    className="mt-3",
)


tab3_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.H4(className="card-title",id="tab_len"),
                    ),
                    dbc.Col(
                        dbc.Button("Download", color="primary",style={"float":"right"},id="download_button",external_link=True),
                        # html.A("Download", style={"float":"right"},id="download_button"),
                    )
                ]                
            ),
            # html.P(id="tab_len_2"),
            html.Br(),
            html.Div(id="visu_tab_data",style={'height': '600px','overflow': 'scroll'}),
            html.Div(id='intermediate_value', style={'display': 'none'})
            # dbc.Button("Click here", color="success"),
        ]        
    ),
    className="mt-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Overview",tab_id="Overview"),
        dbc.Tab(tab2_content, label="Map",tab_id="Map"),
        dbc.Tab(tab3_content, label="Export",tab_id="Export")
    ],
    card=True,
    active_tab="Map"
)

# main layout
app.layout = dbc.Container(
            [
                html.H1("Capillarité Orange Niger",className="display-5",style={'margin-top':'2rem'}),
                # logo,
                html.Hr(className="dash-bootstrap",style={'margin-bottom':'2rem','border-top': '1px solid rgb(200,200,200)'}),
                dbc.Row(
                    [
                        dbc.Col(controls, md=4),
                        dbc.Col(tabs, md=8),
                    ],
                    align="top",
                ),
            ],
            fluid=True
        )


# Back End ---------------------------------------------------------------------

# Zone filtered options
@app.callback(
    Output("zone_selector", "options"), 
        [
            Input("dacr_selector", "value")
        ]
    )
def zoning_options(selected_dacrs):
    zones = list(zoning[zoning['DACR'].isin(selected_dacrs)]['ZONE'].unique())
    return [{'label': zone, 'value': zone} for zone in zones]


# Sector filtered options
@app.callback(
    Output("sector_selector", "options"), 
        [
            Input("dacr_selector", "value")
        ]
    )
def sector_options(selected_dacrs):
    sectors = list(zoning[zoning['DACR'].isin(selected_dacrs)]['SECTEUR'].unique())
    return [{'label': sector, 'value': sector} for sector in sectors]


# Filter and clean data
@app.callback(
    Output("intermediate_value", "children"),
    [
        Input("submit_button", "n_clicks")
    ],
    [
        State("date_selector", "date"),
        State("global_om_status_selector", "value"),
        State("cashx_status_selector", "value"),
        State("oos_status_selector", "value"),
        State("dacr_selector", "value"),
        State("zone_selector", "value"),
        State("sector_selector", "value")
    ]
)
def filter_data(n_clicks,selected_date,pos_globla_status,pos_cx_status,pos_oos_status,selected_dacrs,selected_zones,selected_sectors):
    # apply date filter
    selected_date = datetime.strptime(selected_date[:10],"%Y-%m-%d")
    fdf = df[df['DATE'] == selected_date]
    # apply pos global status filter
    if len(pos_globla_status) > 0:
        fdf = fdf[fdf['POS_STATUS'].isin(pos_globla_status)]
    # apply pos cx status
    if len(pos_cx_status) > 0:
        fdf = fdf[fdf['CASH_IN_OUT_STATUS'].isin(pos_cx_status)]
    # apply dacr filter
    if len(selected_dacrs) > 0:
        fdf = fdf[fdf['DACR'].isin(selected_dacrs)]
    # apply zone filters
    if len(selected_zones) > 0:
        fdf = fdf[fdf['ZONE'].isin(selected_zones)]
    # apply sector filters
    if len(selected_sectors) > 0:
        fdf = fdf[fdf['SECTEUR'].isin(selected_sectors)]
    #    
    if fdf.shape[0] > 0:
        save_file(filename='extract.csv', fdf = fdf)
        filtered_data = fdf.to_json()
    else:
        Path(os.path.join(UPLOAD_DIRECTORY, "extract.csv"),exist_ok=True).touch()
        filtered_data = None

    return filtered_data


# Refesh tab visu
@app.callback(
    Output("visu_tab_data", "children"),
    [
        Input("intermediate_value", "children")
    ]
)
def refresh_tab_data(jsonified_cleaned_data):
    fdf = pd.read_json(jsonified_cleaned_data) 
    if fdf.shape[0] > 0:
        fdf.rename(
            columns = {
                'POS': 'PDV',
                'POS_CAT': 'CATEGORIE',
                'POS_CHANNEL': 'CANAL',
                'POS_GROUP': 'GROUPE',
                'POS_STATUS': 'STATUT GLOBAL',
                'LAST_TR_DATE': 'DATE DERNIERE TRANSACTION',
                'CASH_IN_OUT_STATUS': 'STATUT CASH INOUT',
                'LAST_CI_DATE': 'DATE DERNIER CASH IN',
                'LAST_CO_DATE': 'DATE DERNIER CASH OUT',
            },
            inplace=True
        )

        fdf = fdf[['PDV','DATE','CATEGORIE', 'CANAL', 'GROUPE', 'STATUT GLOBAL', 'STATUT CASH INOUT', 'DACR','ZONE', 'SECTEUR']].head(100)
        # fdf["DATE"] = pd.to_datetime(fdf["DATE"])
        tab_data = dbc.Table.from_dataframe(df = fdf, striped=True, bordered=True, hover=True,responsive=True)
    else:
        tab_data = None
    
    return tab_data


# Refesh tab lenght
@app.callback(
    Output("tab_len", "children"),
    [
        Input("intermediate_value", "children")
    ]
)
def refresh_tab_data(jsonified_cleaned_data):    
    return "{0} résultat(s) trouvé(s)...".format(f"{pd.read_json(jsonified_cleaned_data).shape[0]:,}".replace(',',' '))


# Map
def gen_map_layout(center_lon,center_lat,zomm_start):
    return dict(
        autosize=True,
        automargin=True,
        height=600,
        # margin=dict(l=30, r=30, b=20, t=40),
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=True,
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        legend=dict(font=dict(size=14), orientation="h"),
        # title="Satellite Overview",
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style="light",
            center=dict(lon=center_lon, lat=center_lat),
            zoom=zomm_start,
        ),
    )

def gen_map(map_data):
    # groupby returns a dictionary mapping the values of the first field
    # 'classification' onto a list of record dictionaries with that
    # classification value.
    longitudes = [float(x) for x in map_data['LONGITUDE']]
    latitudes = [float(x) for x in map_data['LATITUDE']]
    status_list = list(map_data['POS_STATUS'].unique())

    traces = []
    for status in status_list:
        fdf2 = map_data[map_data['POS_STATUS'] == status]
        trace = dict(
            type="scattermapbox",
            lon=[float(x) for x in fdf2['LONGITUDE']],
            lat=[float(x) for x in fdf2['LATITUDE']],
            hoverinfo='text',
            text=[["PDV: {0} <br>LOCALITE: {1} <br>DACR: {2} <br>ZONE: {3} <br>SECTEUR: {4}".format(i,j,k,l,m)]
                                for i,j,k,l,m in zip(map_data['POS'], map_data['LOCALITE'],map_data['DACR'],map_data['ZONE'],map_data['SECTEUR'])],
            customdata=fdf2["POS"],
            name=status,
            marker=dict(
                size=7, 
                opacity=0.6,
                color=[markers_colors[status] for status in fdf2['POS_STATUS']]
            ),
        )
        traces.append(trace)

    figure = dict(
        data=traces, 
        layout=gen_map_layout(center_lon = np.mean(longitudes),center_lat = np.mean(latitudes), zomm_start = 7)
    )
    return figure


# Refesh Map
@app.callback(
    Output("mapbox_fig", "figure"),
    [
        Input("intermediate_value", "children")
    ]
)
def refresh_map(jsonified_cleaned_data):
    source_data = pd.read_json(jsonified_cleaned_data)
    # tmp = list(source_data['LATITUDE'])
    # lat = [float(x) for x in tmp]
    # tmp = list(source_data['LONGITUDE'])
    # lon = [float(x) for x in tmp]
    # popup = list(source_data['POS'])
    return gen_map(source_data)






# Export to csv *************************************************************************************************

def save_file(filename, fdf):
    """Save result to csv"""
    file_spec = os.path.join(UPLOAD_DIRECTORY, filename)
    fdf.to_csv(
        path_or_buf=file_spec,
        sep=";",
        decimal=".",
        na_rep="",
        index =False,
        encoding ='utf-8',
        date_format='%Y-%m-%d',
        # compression = 'gzip'
    )


def file_download_link(filename='extract.csv'):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    # return html.A(filename, href=location)
    return location


@app.callback(
    Output("download_button", "href"),
    [
        Input("submit_button", "n_clicks")
    ]
)
def update_output(n_clicks):
    """Save uploaded files and regenerate the file list."""
    # save_file(filename='extract.csv', fdf = zoning)
    return file_download_link(filename='extract.csv')


# Fonctionnalié *************************************************************************************************







if __name__ == "__main__":
    app.run_server(debug=True)
