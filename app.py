# package imports
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash import no_update
from flask import session, copy_current_request_context

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
import json
# import dash_table
import dash_auth
import plotly.figure_factory as ff
import plotly.express as px


#
import sys
# sys.path.append('/var/www/DashApps/FlaskApp/FlaskApp/')
from controls import overview_layout,mapbox_access_token,cached_columns,MONTH_NAMES,format_int
from controls import ACTIVITIES, activity_options,STATUS, status_options,OM_CX_CATEGORIES,om_cx_category_options
from controls import MAP_THEMES_VALUES,MAP_THEMES_LABEL,map_theme_options,COLORS,tab_columns_rename,status_markers_colors,impact_markers_colors,commission_markers_colors


# local imports
from auth import authenticate_user, validate_login_session
from server import app, server

# Function for export to csv ability
@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


#*****************************************************************************************************************************


# Get relative path : data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
UPLOAD_DIRECTORY = PATH.joinpath("app_uploaded_files").resolve()

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


# init export file
Path(os.path.join(UPLOAD_DIRECTORY, "extract.csv"),exist_ok=True).touch()


# Dates options
date_df = pd.read_csv(DATA_PATH.joinpath("upsales_app.csv"),sep=";",usecols = ['DATE','MONTH']).drop_duplicates(keep='first') #low_memory=False)
date_df["DATE"] = pd.to_datetime(date_df["DATE"])
date_df["MONTH"] = pd.to_datetime(date_df["MONTH"])
MONTHS = [MONTH_NAMES[pd.to_datetime(x).strftime('%B')] + ' ' + pd.to_datetime(x).strftime('%Y') for x in date_df['MONTH'].unique()]
MonthSup = MONTH_NAMES[pd.to_datetime(date_df['MONTH'].max()).strftime('%B')] + ' ' + pd.to_datetime(date_df['MONTH'].max()).strftime('%Y')
MonthSupValue  = pd.to_datetime(date_df['MONTH'].max()).strftime('%Y-%m-%d')
DateSup  = pd.to_datetime(date_df['DATE'].max()).strftime('%d') + ' ' + MONTH_NAMES[pd.to_datetime(date_df['DATE'].max()).strftime('%B')].lower() + ' ' + pd.to_datetime(date_df['DATE'].max()).strftime('%Y')
month_options = [
    {
        "label": MONTH_NAMES[pd.to_datetime(month).strftime('%B')] + ' ' + pd.to_datetime(month).strftime('%Y'), 
        "value": pd.to_datetime(month).strftime('%Y-%m-%d')
    } for month in date_df['MONTH'].unique()
]


# Data for geo options
zoning = pd.read_csv(DATA_PATH.joinpath("out_ref_sites.csv"),sep=";") #low_memory=False)
zoning = zoning[['DACR','ZONE','SECTEUR']].drop_duplicates(keep='first')

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





def serve_layout():
    # session_id = str(uuid.uuid4())
    
    # App main form ****************************
    controls = dbc.Card(
        [
            # Month Dropdown selector
            dbc.FormGroup(
                [
                    dbc.Label("Mois",style={'margin-right':'0.5rem','marging-top' : '3rem'}),
                    html.Br(),
                    dcc.Dropdown(
                        id="month_selector",
                        options=month_options,
                        placeholder="Select a month",
                        disabled=False,
                        multi=False,
                        value=MonthSupValue,
                        className="dash-bootstrap"
                    ),

                    # dcc.DatePickerSingle(
                    #    id='date_selector',
                    #    min_date_allowed=date_inf,
                    #    max_date_allowed=date_sup,
                    #    initial_visible_month=current_date,
                    #    date=current_date,
                    #    display_format="DD/MM/YYYY",
                    #    className="dash-bootstrap"
                    # ),
                ]
            ),

            # Activity selector
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

            # Global pos status selector
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
            
            # Cash In/Out status selector
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
            
            # Commission perf selector
            dbc.FormGroup(
                [
                    html.Br(),
                    # html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(135,153,153)'}),
                    dbc.Label("Commissions mesnuelles ≥ 1 000F"),
                    dbc.Checklist(
                        options=[{'label': 'Oui', 'value': 'Oui'},{'label': 'Non', 'value': 'Non'}],
                        value=['Oui','Non'],
                        id="commission_status_selector",
                        # switch=True,
                        inline=True
                    ),
                ]
            ),

            # DACR selector
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
            
            # Zone selector
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
            
            # Sector selector
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
            
            
            # Submit button
            dbc.FormGroup(
                [
                    html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(135,153,153)'}),
                    dbc.Button("Valider", id="submit_button", className="mr-2",style={'display': 'inline-block','float':'right'}),
                    # dbc.Button("Out", id="zzz", className="mr-2",style={'display': 'inline-block','float':'left'}),
                    # html.Span(id="example-output", style={"vertical-align": "middle"}),
                ]
            ),
        ],
        body=True,
    )


    # App Visu tabs ****************************
    # Overview tab content
    tab1_content = dbc.Card(
        dbc.CardBody(
            [
                # html.P("Overview", className="card-text"),
                # dbc.Button("Click here", color="success"),
                overview_layout,
            ],
            id="visu_overview"
        ),
        className="mt-3",
    )

    # Map tab content
    tab2_content = dbc.Card(
        dbc.CardBody(
            [
                dbc.FormGroup(
                    [
                        html.H4("Axe d'analyse ... ",className="card-title",style={'width':'50%','float':'left'}),
                        dcc.Dropdown(
                            id="map_theme_selector",
                            placeholder="Select theme",
                            options=map_theme_options,
                            multi=False,
                            value=MAP_THEMES_VALUES[0],
                            style={'width':'50%','float':'right'}
                        ),
                    ]
                ),
                html.Br(),
                html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(200,200,200)'}),
                html.Br(),
                # html.P("Map", className="card-text"),
                dcc.Graph(id="mapbox_fig"),
                html.Br(), 
                html.Br(),
                html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(200,200,200)'}),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H4(className="card-title",id="map_selection_tab_len"),
                        )
                    ]                
                ),
                html.Br(),
                html.Div(id="map_selected_tab_data",style={'height': '400px','overflow': 'scroll'}),
                # html.Pre(id="map_selected_tab_data",style={'paddingTop': 35}),
            ],
            id="visu_map"
        ),
        
        className="mt-3",
    )

    # Export tab data to csv content
    tab3_content = dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.H4(className="card-title",id="export_tab_len"),
                        ),
                        dbc.Col(
                            dbc.Button("Download", color="primary",style={"float":"right"},id="download_button",external_link=True),
                            # html.A("Download", style={"float":"right"},id="download_button"),
                        )
                    ]                
                ),
                # html.P(id="tab_len_2"),
                html.Br(),
                html.Div(id="export_tab_data",style={'height': '600px','overflow': 'scroll'}),
                # html.Div(id='intermediate_value', style={'display': 'none'}),
                # html.Div(id='intermediate_value2', style={'display': 'none'}),
                # dbc.Button("Click here", color="success"),
                dcc.Store(id='intermediate_value', storage_type='session'),
                dcc.Store(id='intermediate_value2', storage_type='session')
            ]        
        ),
        className="mt-3",
    )


    # All tabs toguether
    tabs = dbc.Tabs(
        [
            dbc.Tab(tab1_content, label="Overview",tab_id="Overview"),
            dbc.Tab(tab2_content, label="Map",tab_id="Map"),
            dbc.Tab(tab3_content, label="Export",tab_id="Export")
        ],
        card=True,
        active_tab="Overview"
    )

    logout_button = dbc.Row(
        [
            # dbc.Col(dbc.Input(type="search", placeholder="Search")),
            dbc.Col(
                dbc.Button(id='logout_btn',children="Logout", color="danger", className="ml-2"),
                width="auto",
            ),
        ],
        no_gutters=True,
        className="ml-auto flex-nowrap mt-3 mt-md-0",
        align="center",
    )

    # Main top bar
    navbar = dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=app.get_asset_url("logo_upsales.jfif"), height="60px"),md=3),
                        dbc.Col(dbc.NavbarBrand("Capillarité Orange Money | {0}".format(DateSup), className="ml-2",style={"font-weight": "bold","fontSize": "2rem"})),
                    ],
                    align="center",
                    no_gutters=True
                ),
            ),
            dbc.Collapse(logout_button, id="navbar-collapse", navbar=True)
        ],
        color="light",
        dark=False,
    )

    # main layout
    final_layout = dbc.Container(
        [
            # logo,
            # html.H1("Capillarité Orange Money",style={'margin': 0}), 
            dcc.Location(id='home-url',pathname='/home'),    
            navbar,  
            html.Br(),  
            html.Br(),       
            # html.Hr(className="dash-bootstrap",style={'margin-bottom':'2rem','border-top': '1px solid rgb(200,200,200)'}),
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

    return final_layout


#*****************************************************************************************************************************

# login layout content
def login_layout():
    return html.Div(
        [
            dcc.Location(id='login-url',pathname='/login',refresh=False),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.H4('Login',className='card-title'),
                                    dbc.Input(id='login-email',placeholder='User'),
                                    dbc.Input(id='login-password',placeholder='Assigned password',type='password'),
                                    dbc.Button('Submit',id='login-button',color='success',block=True),
                                    html.Br(),
                                    html.Div(id='login-alert')
                                ],
                                body=True
                            ),
                            width=6
                        ),
                        justify='center'
                    )
                ]
            )
        ]
    )

# home layout content
@validate_login_session
def app_layout():
    return \
        serve_layout()

# main app layout
app.layout = html.Div(
    [
        dcc.Location(id='url',refresh=False),
        html.Div(
            login_layout(),
            id='page-content'
        ),
    ]
)


###############################################################################
# utilities
###############################################################################

# router
@app.callback(
    Output('page-content','children'),
    [Input('url','pathname')]
)
def router(url):
    if url=='/home':
        return app_layout()
    elif url=='/login':
        return login_layout()
    else:
        return login_layout()

# authenticate 
@app.callback(
    [Output('url','pathname'),
     Output('login-alert','children')],
    [Input('login-button','n_clicks')],
    [State('login-email','value'),
     State('login-password','value')])
def login_auth(n_clicks,email,pw):
    '''
    check credentials
    if correct, authenticate the session
    otherwise, authenticate the session and send user to login
    '''
    if n_clicks is None or n_clicks==0:
        return no_update,no_update
    credentials = {'user':email,"password":pw}
    if authenticate_user(credentials):
        session['authed'] = True
        return '/home',''
    session['authed'] = False
    return no_update,dbc.Alert('Incorrect credentials.',color='danger',dismissable=True)

@app.callback(
    Output('home-url','pathname'),
    [Input('logout_btn','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    return '/login'


###############################################################################
# callbacks
###############################################################################

# Drildown geo
@app.callback(
    Output("zone_selector", "options"),
    [
        Input("dacr_selector", "value")
    ]
)
def down_to_zones(selected_dacrs):
    zones = list(zoning[zoning['DACR'].isin(selected_dacrs)]['ZONE'].unique())
    return [{'label': zone, 'value': zone} for zone in zones]

@app.callback(
    Output("sector_selector", "options"),
    [
        Input("dacr_selector", "value"),
        Input("zone_selector", "value")
    ]
)
def down_to_sectors(selected_dacrs,selected_zones):
    tmp = zoning[zoning['DACR'].isin(selected_dacrs)]
    tmp = tmp[tmp['ZONE'].isin(selected_zones)]
    sectors = list(tmp['SECTEUR'].unique())
    return [{'label': sector, 'value': sector} for sector in sectors]



# Cache cleaned data in hiden div
@app.callback(
    Output("intermediate_value", "data"),
    [
        Input("submit_button", "n_clicks")
    ],
    [
        State("month_selector", "value"),
        State("global_om_status_selector", "value"),
        State("cashx_status_selector", "value"),
        State("commission_status_selector", "value"),
        State("dacr_selector", "value"),
        State("zone_selector", "value"),
        State("sector_selector", "value")
    ]
)
def filter_data(n_clicks,selected_month,pos_globla_status,pos_cx_status,pos_commission_status,selected_dacrs,selected_zones,selected_sectors):
    # Load main data
    df = pd.read_csv(DATA_PATH.joinpath("upsales_app.csv"),sep=";") #low_memory=False)
    df["DATE"] = pd.to_datetime(df["DATE"])
    df["MONTH"] = pd.to_datetime(df["MONTH"])
    # apply date filter
    selected_month = datetime.strptime(selected_month[:10],"%Y-%m-%d")
    fdf = df[df['MONTH'] == selected_month]
    # apply pos global status filter
    if len(pos_globla_status) > 0:
        fdf = fdf[fdf['POS_STATUS'].isin(pos_globla_status)]
    # apply pos cx status
    if len(pos_cx_status) > 0:
        fdf = fdf[fdf['CASH_IN_OUT_STATUS'].isin(pos_cx_status)]
    # apply pos commission status
    if len(pos_commission_status) > 0:
        fdf = fdf[fdf['COMMISSION_PERF'].isin(pos_commission_status)]
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
        fdf = fdf[cached_columns]
        save_file(filename='extract.csv', fdf = fdf)
        filtered_data = fdf.to_json()
        # filtered_data = df.to_json(date_format='iso', orient='split')  # pd.read_json(query_data(), orient='split')        
    else:
        Path(os.path.join(UPLOAD_DIRECTORY, "extract.csv"),exist_ok=True).touch()
        filtered_data = None

    return filtered_data 





# Refesh Export table
@app.callback(
    [
        Output("export_tab_data", "children"),
        Output("export_tab_len", "children")
    ],
    [
        Input("intermediate_value", "data")
    ]
)
def refresh_export_tab_data(jsonified_cleaned_data):
    displayed_columns = ['PDV','MOIS','DATE STATUT','CATEGORIE', 'CANAL', 'STATUT', 'DERNIERE TRANSAC.','DERNIERE VISITE','IMPACTE VISITE','COMMISSIONS','DACR','ZONE', 'SECTEUR']
    fdf = pd.read_json(jsonified_cleaned_data) 
    fdf['MONTH'] = [MONTH_NAMES[dt.datetime.fromtimestamp(x / 1e3).strftime("%b.")].lower() + dt.datetime.fromtimestamp(x / 1e3).strftime("-%y") for x in fdf['MONTH']]
    fdf['DATE'] = [x.strftime('%Y-%m-%d') for x in fdf['DATE']]
    fdf = fdf.replace({"LAST_VISITE_DATE" : '1970-01-01'},np.nan)
    fdf = fdf.replace({"IMPACT_VISITE" : '-'},np.nan)
    if fdf.shape[0] > 0:
        fdf.rename(
            columns = tab_columns_rename,
            inplace=True
        )        
        fdf = fdf[displayed_columns] # .head(100)        
    else:
        fdf = pd.DataFrame()
    
    # responsive='md'
    return dbc.Table.from_dataframe(df = fdf, striped=True, bordered=True, hover=True),"{0} résultat(s) selectionné(s)...".format(format_int(pd.read_json(jsonified_cleaned_data).shape[0]))




# Generate Map Layout
def gen_map_layout(center_lon,center_lat,zomm_start):
    return dict(
        autosize=True,
        automargin=True,
        height=600,
        # width='100%',
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


def gen_map_content(map_data,map_theme):
    # groupby returns a dictionary mapping the values of the first field
    # 'classification' onto a list of record dictionaries with that
    # classification value.
    longitudes = [float(x) for x in map_data['LONGITUDE']]
    latitudes = [float(x) for x in map_data['LATITUDE']]
    status_options = list(map_data['POS_STATUS'].unique())
    visit_impact_options = list(map_data['IMPACT_VISITE'].unique())
    commission_perf_options = list(map_data['COMMISSION_PERF'].unique())

    # Theme = Status des PDVs
    if map_theme == "Status des PDVs":
        traces = []
        for status in status_options:
            fdf2 = map_data[map_data['POS_STATUS'] == status]
            trace = dict(
                type="scattermapbox",
                lon=[float(x) for x in fdf2['LONGITUDE']],
                lat=[float(x) for x in fdf2['LATITUDE']],
                hoverinfo='text',
                text=[["""PDV: {0} <br>CATEGORIE: {1} <br>CANAL: {2} <br>STATUS: {3} <br>STATUS CASH IN/OUT: {4} <br>COMMISSIONS: {5} <br>DERNIERE TRANSACTION: {6} <br>DERNIERE VISITE: {7} <br>IMPACT VISITE: {8} <br>SITE: {9} <br>LOCALITE: {10} <br>DACR: {11} <br>ZONE: {12} <br>SECTEUR: {13} <br>""".format(a,b,c,d,e,f,g,h,i,j,k,l,m,n)]
                                    for a,b,c,d,e,f,g,h,i,j,k,l,m,n in zip(
                                        fdf2['POS'], 
                                        fdf2['POS_CAT'],
                                        fdf2['POS_CHANNEL'],
                                        fdf2['POS_STATUS'],
                                        fdf2['CASH_IN_OUT_STATUS'],
                                        fdf2['COMMISSIONS_AMNT'],
                                        fdf2['LAST_TR_DATE'],
                                        fdf2['LAST_VISITE_DATE'],
                                        fdf2['IMPACT_VISITE'],
                                        fdf2['SITE'],
                                        fdf2['LOCALITE'],
                                        fdf2['DACR'],
                                        fdf2['ZONE'],
                                        fdf2['SECTEUR'])],
                customdata=fdf2["POS"],
                name=status,
                marker=dict(
                    size=7, 
                    opacity=0.6,
                    color=[status_markers_colors[x] for x in fdf2['POS_STATUS']]
                ),
            )
            traces.append(trace)

            figure = dict(
            data=traces, 
            layout=gen_map_layout(center_lon = np.mean(longitudes),center_lat = np.mean(latitudes), zomm_start = 7)
        )

    # Theme = Impact des visites
    if map_theme == "Impact des visites":
        traces = []
        for impact in visit_impact_options:
            fdf2 = map_data[map_data['IMPACT_VISITE'] == impact]
            trace = dict(
                type="scattermapbox",
                lon=[float(x) for x in fdf2['LONGITUDE']],
                lat=[float(x) for x in fdf2['LATITUDE']],
                hoverinfo='text',
                text=[["""PDV: {0} <br>CATEGORIE: {1} <br>CANAL: {2} <br>STATUS: {3} <br>STATUS CASH IN/OUT: {4} <br>COMMISSIONS: {5} <br>DERNIERE TRANSACTION: {6} <br>DERNIERE VISITE: {7} <br>IMPACT VISITE: {8} <br>SITE: {9} <br>LOCALITE: {10} <br>DACR: {11} <br>ZONE: {12} <br>SECTEUR: {13} <br>""".format(a,b,c,d,e,f,g,h,i,j,k,l,m,n)]
                                    for a,b,c,d,e,f,g,h,i,j,k,l,m,n in zip(
                                        fdf2['POS'], 
                                        fdf2['POS_CAT'],
                                        fdf2['POS_CHANNEL'],
                                        fdf2['POS_STATUS'],
                                        fdf2['CASH_IN_OUT_STATUS'],
                                        fdf2['COMMISSIONS_AMNT'],
                                        fdf2['LAST_TR_DATE'],
                                        fdf2['LAST_VISITE_DATE'],
                                        fdf2['IMPACT_VISITE'],
                                        fdf2['SITE'],
                                        fdf2['LOCALITE'],
                                        fdf2['DACR'],
                                        fdf2['ZONE'],
                                        fdf2['SECTEUR'])],
                customdata=fdf2["POS"],
                name=impact,
                marker=dict(
                    size=7, 
                    opacity=0.6,
                    color=[impact_markers_colors[x] for x in fdf2['IMPACT_VISITE']]
                ),
            )
            traces.append(trace)

        figure = dict(
            data=traces, 
            layout=gen_map_layout(center_lon = np.mean(longitudes),center_lat = np.mean(latitudes), zomm_start = 7)
        )

    # Theme = Commissions
    if map_theme == "Commissions":
        traces = []
        for commission_perf in commission_perf_options:
            fdf2 = map_data[map_data['COMMISSION_PERF'] == commission_perf]
            trace = dict(
                type="scattermapbox",
                lon=[float(x) for x in fdf2['LONGITUDE']],
                lat=[float(x) for x in fdf2['LATITUDE']],
                hoverinfo='text',
                text=[["""PDV: {0} <br>CATEGORIE: {1} <br>CANAL: {2} <br>STATUS: {3} <br>STATUS CASH IN/OUT: {4} <br>COMMISSIONS: {5} <br>DERNIERE TRANSACTION: {6} <br>DERNIERE VISITE: {7} <br>IMPACT VISITE: {8} <br>SITE: {9} <br>LOCALITE: {10} <br>DACR: {11} <br>ZONE: {12} <br>SECTEUR: {13} <br>""".format(a,b,c,d,e,f,g,h,i,j,k,l,m,n)]
                                    for a,b,c,d,e,f,g,h,i,j,k,l,m,n in zip(
                                        fdf2['POS'], 
                                        fdf2['POS_CAT'],
                                        fdf2['POS_CHANNEL'],
                                        fdf2['POS_STATUS'],
                                        fdf2['CASH_IN_OUT_STATUS'],
                                        fdf2['COMMISSIONS_AMNT'],
                                        fdf2['LAST_TR_DATE'],
                                        fdf2['LAST_VISITE_DATE'],
                                        fdf2['IMPACT_VISITE'],
                                        fdf2['SITE'],
                                        fdf2['LOCALITE'],
                                        fdf2['DACR'],
                                        fdf2['ZONE'],
                                        fdf2['SECTEUR'])],
                customdata=fdf2["POS"],
                name=commission_perf,
                marker=dict(
                    size=7, 
                    opacity=0.6,
                    color=[commission_markers_colors[x] for x in fdf2['COMMISSION_PERF']]
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
        Input("intermediate_value", "data"),
        Input("map_theme_selector", "value")
    ]
)
def refresh_map(jsonified_cleaned_data,map_theme):
    source_data = pd.read_json(jsonified_cleaned_data)
    return gen_map_content(source_data,map_theme)



@app.callback(
    Output('map_selected_tab_data', 'children'),
    [
        Input('mapbox_fig', 'selectedData'),
        Input('intermediate_value', 'data'),
    ]
)
def map_selected_data_table(selectedData, jsonified_cleaned_data):
    displayed_columns = ['PDV','MOIS','CATEGORIE', 'CANAL', 'STATUT', 'DERNIERE TRANSAC.','DERNIERE VISITE','IMPACTE VISITE','COMMISSIONS','DACR','ZONE', 'SECTEUR']
    if json.dumps(selectedData) != 'null':
        json_str = json.dumps(selectedData,indent=2)
        json_obj = json.loads(json_str)
        selected_pos = list(set([x['customdata'] for x in json_obj['points']]))
        fdf = pd.read_json(jsonified_cleaned_data)
        fdf = fdf[fdf['POS'].isin(selected_pos)]

    else:
        # selected_pos = []
        fdf = pd.DataFrame()

    #
    # fdf = pd.read_json(jsonified_cleaned_data) 
    if fdf.shape[0] > 0:
        # current_locale = locale.getlocale(locale.LC_ALL) # get current locale
        # locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
        # fdf = fdf[fdf['POS'].isin(selected_pos)]
        fdf['MONTH'] = [MONTH_NAMES[dt.datetime.fromtimestamp(x / 1e3).strftime("%b.")].lower() + dt.datetime.fromtimestamp(x / 1e3).strftime("-%y")  for x in fdf['MONTH']]
        fdf['DATE'] = [x.strftime('%Y-%m-%d') for x in fdf['DATE']]
        fdf = fdf.replace({"LAST_VISITE_DATE" : '1970-01-01'},np.nan)
        fdf = fdf.replace({"IMPACT_VISITE" : '-'},np.nan)
        fdf.rename(
            columns=tab_columns_rename,
            inplace=True        
        )        
        fdf = fdf[displayed_columns]    
        # locale.setlocale(locale.LC_ALL, current_locale) # restore saved locale    
    else:
        # fdf = pd.DataFrame(columns = displayed_columns)
        fdf = pd.DataFrame()
    
    # ,responsive='md'
    return dbc.Table.from_dataframe(df = fdf, striped=True, bordered=True, hover=True)



@app.callback(
    Output('map_selection_tab_len', 'children'),
    [
        Input('mapbox_fig', 'selectedData')
    ]
)
def map_selected_cnt(selectedData):  
    if selectedData != None:
        json_str = json.dumps(selectedData,indent=2)
        json_obj = json.loads(json_str)
        selected_pos = list(set([x['customdata'] for x in json_obj['points']]))
    else:
        selected_pos = []  
    return "{0} résultat(s) selectionné(s)...".format(format_int(len(selected_pos)))



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


@app.callback(
    [
        Output('overview_dacr_chart','figure'),
        Output('overview_main_comment_main_str','children'),
        Output('overview_main_comment_detail_str','children')
    ],
    [
        Input('intermediate_value', 'data'),
        Input('overwiew_axe_selector', 'value')
    ]
)
def refresh_overview_dacr_chart(jsonified_cleaned_data,selected_axis):
    if json.dumps(jsonified_cleaned_data,indent=2) == "null":
        return px.sunburst()         #emptyFig()
    # Axe definition
    if selected_axis == 'Statut des PDVs':
        analysis_axis = 'POS_STATUS'
    else:
        analysis_axis = 'IMPACT_VISITE'

    # Load and filter data
    df2 = pd.read_json(jsonified_cleaned_data)
    status_date  = pd.to_datetime(df2['DATE'].max()).strftime('%d') + ' ' + MONTH_NAMES[pd.to_datetime(df2['DATE'].max()).strftime('%B')].lower() + ' ' + pd.to_datetime(df2['DATE'].max()).strftime('%Y')
    status_month  = MONTH_NAMES[pd.to_datetime(df2['DATE'].max()).strftime('%B')].lower() + ' ' + pd.to_datetime(df2['DATE'].max()).strftime('%Y')
    # DACR POS CNT
    dacr_data = (
    df2
    .groupby(['MONTH','DACR',analysis_axis])
    .agg({"POS" : "nunique"})
    .reset_index()
    .rename(columns={"POS" : "NOMBRE DE PDVs"})
    # .pivot(index="DACR",columns='POS_STATUS',values='POS_CNT')
    # .reset_index()
    )

    # Chart colo dict
    if selected_axis == 'Statut des PDVs':
        chart_color_dict = {x:status_markers_colors[x] for x in dacr_data[analysis_axis]}
    else:
        chart_color_dict = {x:impact_markers_colors[x] for x in dacr_data[analysis_axis]}

    # Chart
    fig = px.sunburst(dacr_data, path=['DACR', analysis_axis], values='NOMBRE DE PDVs', color=analysis_axis,color_discrete_map=chart_color_dict)
    fig.update_layout(
        margin = dict(t=5, l=5, r=5, b=5)
        # color  = [x:status_markers_colors[x] for x in dacr_data['POS_STATUS']]
    )


    # Overview comments
    if selected_axis == 'Statut des PDVs':
        main_str = """
        {0} PDV(s) actif(s) au {1}.
        """.format(
            format_int(dacr_data[dacr_data['POS_STATUS'].isin(['Actif','Futur inactif'])]['NOMBRE DE PDVs'].sum()),
            status_date
        )
        detail_str = """
        {0} actif(s) et {1} futur inactis(s).
        """.format(
            format_int(dacr_data[dacr_data['POS_STATUS'].isin(['Actif'])]['NOMBRE DE PDVs'].sum()),
            format_int(dacr_data[dacr_data['POS_STATUS'].isin(['Futur inactif'])]['NOMBRE DE PDVs'].sum())
        )
    else:
        main_str = """
        {0} PDV(s) ont été visités en {1}.
        """.format(
            format_int(dacr_data[dacr_data['IMPACT_VISITE'].isin(["N'a pas réagi", 'A réagi','Nouveau PDV visité', 'A maintenu son statut'])]['NOMBRE DE PDVs'].sum()),
            status_month
        )
        detail_str = """
        {0} ont réagi suite à la visite, {1} ont maintenu leur statut, {2} n'ont pas réagi et {3} nouveaux PDV visités.  
        """.format(
            format_int(dacr_data[dacr_data['IMPACT_VISITE'].isin(['A réagi'])]['NOMBRE DE PDVs'].sum()),
            format_int(dacr_data[dacr_data['IMPACT_VISITE'].isin(['A maintenu son statut'])]['NOMBRE DE PDVs'].sum()),
            format_int(dacr_data[dacr_data['IMPACT_VISITE'].isin(["N'a pas réagi"])]['NOMBRE DE PDVs'].sum()),
            format_int(dacr_data[dacr_data['IMPACT_VISITE'].isin(['Nouveau PDV visité'])]['NOMBRE DE PDVs'].sum()),
        )

    return fig, main_str, detail_str






@app.callback(
    [
        Output('overview_zone_chart','figure'),
        Output('intermediate_value2','data'),
        Output('zone_chart_title', 'children')
    ],    
    [
        Input('intermediate_value', 'data'),
        Input('overview_dacr_chart', 'clickData'),
        Input('overwiew_axe_selector', 'value')
    ]
)
def refresh_overview_zone_chart(jsonified_cleaned_data,clickData,selected_axis):
    # Init chart when none click
    if json.dumps(clickData,indent=2) == "null":
        return px.sunburst(), None, None

    # Axe definition 
    geo_axis = "ZONE"   
    if selected_axis == 'Statut des PDVs':
        analysis_axis = 'POS_STATUS'
    else:
        analysis_axis = 'IMPACT_VISITE'

    # Clicked DACR
    if clickData['points'][0]['currentPath'] == '/':
        dacr_name = clickData['points'][0]['id']
    elif clickData['points'][0]['currentPath'] in ['/Agadez/','/Diffa/','/Dosso/','/Maradi/','/Niamey/','/Tahoua/','/Tillaberi/','/Zinder/']:
        dacr_name = clickData['points'][0]['parent']
    else:
        dacr_name = "Agadez"

    # load pos data
    df2 = pd.read_json(jsonified_cleaned_data)
    df2 = df2[df2['DACR'] == dacr_name]
    filtered_data = df2.to_json()

    # AGG DATA
    dacr_data = (
    df2
    .groupby(['MONTH','DACR',geo_axis,analysis_axis])
    .agg({"POS" : "nunique"})
    .reset_index()
    .rename(columns={"POS" : "NOMBRE DE PDVs"})
    # .pivot(index="DACR",columns='POS_STATUS',values='POS_CNT')
    # .reset_index()
    )

    # Chart color dict
    if selected_axis == 'Statut des PDVs':
        chart_color_dict = {x:status_markers_colors[x] for x in dacr_data[analysis_axis]}
    else:
        chart_color_dict = {x:impact_markers_colors[x] for x in dacr_data[analysis_axis]}

    
    fig = px.sunburst(
        dacr_data, 
        path=[geo_axis, analysis_axis], 
        values='NOMBRE DE PDVs', 
        color=analysis_axis,
        color_discrete_map=chart_color_dict
        # hovertemplate='<extra>{fullData.DACR}</extra>'        
    )
    fig.update_layout(margin = dict(t=5, l=5, r=5, b=5))

    return fig,filtered_data, "Zones de {0}: ".format(dacr_name)





@app.callback(
    [
        Output('overview_sector_chart','figure'),
        Output('sector_chart_title','children'),
    ],  
    [
        Input('intermediate_value2', 'data'),
        Input('overview_zone_chart', 'clickData'),
        Input('overwiew_axe_selector', 'value')
    ]
)
def refresh_overview_sector_chart(jsonified_cleaned_data,clickData,selected_axis):
    # Init chart when none click
    if json.dumps(clickData,indent=2) == "null":
        return px.sunburst(), None

    # Axis definition 
    geo_axis = "SECTEUR"   
    if selected_axis == 'Statut des PDVs':
        analysis_axis = 'POS_STATUS'
    else:
        analysis_axis = 'IMPACT_VISITE'

    # Clicked DACR
    if clickData['points'][0]['currentPath'] == '/':
        zone_name = clickData['points'][0]['id']
    else:
        zone_name = clickData['points'][0]['parent']


    # load pos data
    df2 = pd.read_json(jsonified_cleaned_data)
    df2 = df2[df2['ZONE'] == zone_name]
    dacr_name = list(df2['DACR'].unique())[0]

    # AGG DATA
    zone_data = (
    df2
    .groupby(['MONTH','DACR',geo_axis,analysis_axis])
    .agg({"POS" : "nunique"})
    .reset_index()
    .rename(columns={"POS" : "NOMBRE DE PDVs"})
    # .pivot(index="DACR",columns='POS_STATUS',values='POS_CNT')
    # .reset_index()
    )

    # Chart color dict
    if selected_axis == 'Statut des PDVs':
        chart_color_dict = {x:status_markers_colors[x] for x in zone_data[analysis_axis]}
    else:
        chart_color_dict = {x:impact_markers_colors[x] for x in zone_data[analysis_axis]}

    
    fig = px.sunburst(
        zone_data, 
        path=[geo_axis, analysis_axis], 
        values='NOMBRE DE PDVs', 
        color=analysis_axis,
        color_discrete_map=chart_color_dict
        # hovertemplate='<extra>{fullData.DACR}</extra>'        
    )
    fig.update_layout(margin = dict(t=5, l=5, r=5, b=5))

    return fig, "Secteurs de {0} {1}: ".format(dacr_name,zone_name)

###############################################################################
# run app
###############################################################################

if __name__ == "__main__":
    
    app.run_server(
        debug=True
    )