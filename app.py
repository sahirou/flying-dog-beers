"""
Dash port of Shiny iris k-means example:

https://shiny.rstudio.com/gallery/kmeans-example.html
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
# from sklearn import datasets
# from sklearn.cluster import KMeans
import datetime as dt

COLORS = {
    'foucha' : '#ff00ff'
}


ACTIVITIES = [
    'eRecharge',
    'SIM',
    'SimSwap',
    'Orange Money'
]

STATUS = [
    'Actif',
    'Future inactif',
    'Inactif',
    'Inactif récent',
    'Inactif âgé'
]

ERECHARGE_CATEGORIES = [
    'Performant',
    'Presque performant',
    'Non performant'
]

DACRS = [
    'Agadez',
    'Diffa',
    'Dosso',
    'Maradi',
    'Niamey',
    'Tahoua',
    'Tillaberi',
    'Zinder'
]

ZONES = [
    'Sud',
    'Nord',
    'Est',
    'Ouest'
]

SECTEURS = [
    'Kollo',
    'Gouré',
    'Tanout',
    'Oullam'
]

# Create controls
activity_options = [
    {"label": activity, "value": activity} for activity in ACTIVITIES
]

status_options = [
    {"label": status, "value": status} for status in STATUS
]

erecharge_category_options = [
    {"label": category, "value": category} for category in ERECHARGE_CATEGORIES
]

dacr_options = [
    {"label": dacr, "value": dacr} for dacr in DACRS
]

zone_options = [
    {"label": zone, "value": zone} for zone in ZONES
]

secteur_options = [
    {"label": secteur, "value": secteur} for secteur in SECTEURS
]



# iris_raw = datasets.load_iris()
# iris = pd.DataFrame(iris_raw["data"], columns=iris_raw["feature_names"])

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Capillarité"
server = app.server

controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Date",style={'margin-right':'0.5rem','marging-top' : '3rem'}),
                html.Br(),
                dcc.DatePickerSingle(
                    id='date-picker-single',
                    min_date_allowed=dt.date(2020,1,1),
                    max_date_allowed=dt.date(2020,8,31),
                    initial_visible_month=dt.date(2020,2,1),
                    date=dt.date(2020,8, 25),
                    className="dash-bootstrap"
                ),
            ]
        ),
        dbc.FormGroup(
            [
                html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(135,153,153)'}),
                dbc.Label("Activités"),
                dcc.Dropdown(
                    id="activities",
                    options=activity_options,
                    multi=True,
                    value=[ACTIVITIES[0]],
                ),
            ]
        ),
        # status du PDV sur les activités selectionnées
        dbc.FormGroup(
            [
                dbc.Label("Status"),
                dbc.Checklist(
                    options=status_options,
                    value=['Actif','Future inactif'],
                    id="input-status-erecharge",
                    switch=True,
                    inline=True
                ),
            ]
        ),
        # Categorie eRecharge
        dbc.FormGroup(
            [
                html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(135,153,153)'}),
                dbc.Label("Catégorie eRecharge"),
                dbc.Checklist(
                    options=erecharge_category_options,
                    value=ERECHARGE_CATEGORIES,
                    id="input-category-erecharge",
                    switch=True,
                    inline=True
                ),
            ]
        ),
        # Rupure eRecharge
        dbc.FormGroup(
            [
                # html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(135,153,153)'}),
                html.Br(),
                dbc.Label("Rupture eRecharge"),
                dbc.Checklist(
                    options=[{'label': 'Oui', 'value': 'Oui'},{'label': 'Non', 'value': 'Non'}],
                    value=['Oui','Non'],
                    id="input-rupture-erecharge",
                    # switch=True,
                    inline=True
                ),
            ]
        ),
        # Filtre DACR
        dbc.FormGroup(
            [
                html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(135,153,153)'}),
                # html.P('Filtres Géo',style={'margin-top':'0','text-align': 'right','font-style': 'italic','color':'red'}),
                dbc.Label("Régions"),
                dcc.Checklist(
                    id="dacr_toutes",
                    options=[{'label': 'Toutes', 'value': 'Toutes'}],
                    value=['Toutes'],
                    style={'float': 'right'},
                ),     
                dcc.Dropdown(
                    id="dacr",
                    options=dacr_options,
                    multi=True,
                    value=DACRS
                ),
            ]
        ),
        # Filtre ZONE
        dbc.FormGroup(
            [
                dbc.Label("Zones"),
                dcc.Checklist(
                    id="zone_toutes",
                    options=[{'label': 'Toutes', 'value': 'Toutes'}],
                    value=['Toutes'],
                    style={'float': 'right'},
                ),
                dcc.Dropdown(
                    id="zone",
                    options=zone_options,
                    multi=True,
                    value=ZONES,
                ),
            ]
        ),
        # Filtre SECTEUR
        dbc.FormGroup(
            [
                dbc.Label("Secteurs"),
                dcc.Checklist(
                    id="secteurs_tous",
                    options=[{'label': 'Tous', 'value': 'Tous'}],
                    value=['Tous'],
                    style={'float': 'right'},
                ),
                dcc.Dropdown(
                    id="secteur",
                    options=secteur_options,
                    multi=True,
                    value=[SECTEURS[0]],
                ),
            ]
        ),
        # Submit
        dbc.FormGroup(
            [
                html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(135,153,153)'}),
                dbc.Button("Valider", id="submit", className="mr-2",style={'display': 'inline-block'}),
                # html.Span(id="example-output", style={"vertical-align": "middle"}),
            ]
        ),
    ],
    body=True,
)

# Viz
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Quelques stats", className="card-text"),
            # bc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Carte", className="card-text"),
            # dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Données tabulaires", className="card-text"),
            # dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Overview"),
        dbc.Tab(tab2_content, label="Map"),
        dbc.Tab(tab3_content, label="Données tabulaires"),
    ]
)

# jumbo
jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.H1("Capillarité Orange Niger",className="display-5"),
                html.Hr(className="dash-bootstrap",style={'margin-bottom':'2rem','border-top': '1px solid rgb(255,89,0)'}),
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
    ],
    fluid=True
)

# main layout
app.layout = dbc.Container(
            [
                html.H1("Capillarité Orange Niger",className="display-5",style={'margin-top':'2rem'}),
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



if __name__ == "__main__":
    app.run_server()
