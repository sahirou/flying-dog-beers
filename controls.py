import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

mapbox_access_token = 'pk.eyJ1Ijoic2FuaXJvdSIsImEiOiJja2U0cWwweDEwdnlhMnpsZm9oeWJzNm84In0.Xwoh5FQDOPwq-vUWFqzEcA'

# Form data *********************************

# Overview tab analysis axis options
OVERVIEW_AXIS = [
    'Statut des PDVs',
    'Impact des visites'
]
overwiew_axis_options = [
    {"label": axe, "value": axe} for axe in OVERVIEW_AXIS
]


# POS activities dropdown options
ACTIVITIES = [
    'Orange Money'
]
activity_options = [
    {"label": activity, "value": activity} for activity in ACTIVITIES
]


# POS global stutus options
STATUS = [
    'Actif',
    'Futur inactif',
    'Inactif récent',
    'Inactif âgé'
]
status_options = [
    {"label": status, "value": status} for status in STATUS
]


# POS cash x status options
OM_CX_CATEGORIES = [
    'Performant',
    'Presque performant',
    'Non performant'
]
om_cx_category_options = [
    {"label": category, "value": category} for category in OM_CX_CATEGORIES
]

# Thematic maps options
MAP_THEMES_VALUES = [
    "Status des PDVs",
    "Impact des visites",
    "Commissions"
]
MAP_THEMES_LABEL = {
    "Status des PDVs": "Status des PDVs",
    "Impact des visites": "Impact des visites",
    "Commissions": "Commissions mensuelles ≥ 1 000F"
}
map_theme_options = [
    {"label": MAP_THEMES_LABEL[map_theme], "value": map_theme} for map_theme in MAP_THEMES_VALUES
]


# App colors
COLORS = {
    'green': 'rgb(112,173,71)',                  
    'blue': 'rgb(0,175,240)',            
    'orange': 'rgb(255,89,0)',            
    'red': 'rgb(255,0,0)',
    'black': 'rgb(0,0,0)',
    'lightgray': 'rgb(200,200,200)',
    'darkgray': 'rgb(153,153,153)',
    'fucha': 'rgb(255,0,255)',
    'yellow': 'rgb(255,255,0)'                  
}


# POS status colors
status_markers_colors = {
    'Actif': COLORS['green'],                   
    'Futur inactif': COLORS['blue'],            
    'Inactif récent': COLORS['orange'],           
    'Inactif âgé': COLORS['red'],                 
}

# Visite impact colors
impact_markers_colors = {
    'A réagi': COLORS['green'],                   
    'A maintenu son statut': COLORS['blue'],       
    "N'a pas réagi": COLORS['red'],
    'Jamais visité': COLORS['black'],
    'Non visité' : COLORS['darkgray'],
    "Nouveau PDV visité" : COLORS['orange']
}


# Commissions performance colors
commission_markers_colors = {
    'Oui': COLORS['green'],
    'Non': COLORS['red']
}


# Define coulumns names that appear in tabular data
tab_columns_rename = {
    'POS': 'PDV',
    'MONTH': 'MOIS',
    'DATE': 'DATE STATUT',
    'POS_CAT': 'CATEGORIE',
    'POS_CHANNEL': 'CANAL',
    'POS_GROUP': 'GROUPE',
    'POS_STATUS': 'STATUT',
    'LAST_TR_DATE': 'DERNIERE TRANSAC.',
    'LAST_VISITE_DATE': 'DERNIERE VISITE',
    'IMPACT_VISITE': 'IMPACTE VISITE',
    'COMMISSIONS_AMNT': 'COMMISSIONS'
}


# Overview tab main comment
overview_main_comment = dbc.Jumbotron(
    [
        html.H1(className="display-5",id='overview_main_comment_main_str'), # children= "Jumbotron"
        html.P(
            # "Use a jumbotron to call attention to "
            # "featured content or information.",
            id='overview_main_comment_detail_str',
            className="lead"
        ),
        html.Hr(className="my-2"),
        html.P(
            # "Jumbotrons use utility classes for typography and "
            #"spacing to suit the larger container."
            "Repartition sur les graphes  ci-dessous."
        ),
        # html.P(dbc.Button("Learn more", color="primary"), className="lead"),
    ]
)


# Overview filters
overview_layout = dbc.Card(
    dbc.CardBody(
        [
            dbc.FormGroup(
                [
                    html.H4("Axe d'analyse ...",className="card-title",style={'float':'left'}),
                    dbc.RadioItems(
                        id="overwiew_axe_selector",
                        options=overwiew_axis_options,
                        inline=True,
                        value=OVERVIEW_AXIS[0],
                        style={'float':'right'}
                    )                            
                ]
            ),
            html.Br(),            
            html.Br(), 
            # html.Div(
            #     [
            #         html.P(id='overview_comments')
            #     ]
            # ),
            overview_main_comment,
            html.Div(id='overview_comments'),
            html.Br(),            
            html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(200,200,200)'}),
            html.Br(),
            html.H4("Détails par DACR: ",className="card-title",style={'float':'left'}), 
            html.Br(), 
            # DACR
            dbc.Row(
                [
                    # html.H4(children="DACR Chart",className="card-title",id="overview_dacr_chart_title"),
                    html.Br(),
                    html.Br(),
                    dcc.Graph(
                        id="overview_dacr_chart"  
                    ),
                    html.Br()
                ],justify="center", align="center", className="h-50"
                # style={'justify':'center','align':'center'} 
            ),

            # ZONE
            html.Br(),            
            html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(200,200,200)'}),
            html.Br(),
            html.H4(id="zone_chart_title",className="card-title",style={'float':'left'}),     
            html.Br(), 
            dbc.Row(
                [
                    html.Br(),
                    html.Br(),
                    dcc.Graph(
                        id="overview_zone_chart"
                    ),
                    html.Br(), 
                ], justify="center", align="center", className="h-50"              
            ),


            html.Br(),            
            # SECTOR
            html.Br(),            
            html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(200,200,200)'}),
            html.Br(),
            html.H4(id="sector_chart_title",className="card-title",style={'float':'left'}),     
            html.Br(), 
            dbc.Row(
                [
                    html.Br(),
                    html.Br(),
                    dcc.Graph(
                        id="overview_sector_chart"
                    ),
                    html.Br(), 
                ], justify="center", align="center", className="h-50"              
            ),

            dbc.Row(
               [
                   html.Pre(id='click_data',style={'paddingTop':35})
               ]
            )
        ]        
    ),
    className="mt-3"
)


cached_columns = [
    "POS",
    "MONTH",
    "DATE",
    "POS_CAT",
    "POS_CHANNEL",
    "POS_GROUP",
    "LAST_TR_DATE",
    "POS_STATUS",
    "CASH_IN_OUT_STATUS",
    "SITE",
    "LOCALITE",
    "MILIEU",
    "ZONE",
    "DACR",
    "BALANCE",
    "LONGITUDE",
    "LATITUDE",
    "LOCALISATION",
    "SECTEUR",
    "LAST_VISITE_DATE",
    "VISITE",
    "COMMISSIONS_AMNT",
    "IMPACT_VISITE",
    "COMMISSION_PERF"
]


MONTH_NAMES = {
    'January': 'Janvier',
    'February': 'Février',
    'March' : 'Mars',
    'April' : 'Avril',
    'May' : 'Mai',
    'June' : 'Juin',
    'July' : 'Juillet',
    'August' : 'Août',
    'September' : 'Septembre',
    'October' : 'Octobre',
    'November' : 'Novembre',
    'December': 'Décembre',
    #
    'Jan.': 'Janv.',
    'Feb.': 'Févr.',
    'Mar.' : 'Mars.',
    'Apr.' : 'Avr.',
    'May' : 'Mai.',
    'Jun.' : 'Juin.',
    'Jul.' : 'Juil.',
    'Aug.' : 'Août.',
    'Sep.' : 'Sept.',
    'Oct.' : 'Oct.',
    'Nov.' : 'Nov.',
    'Dec.': 'Déc.'
}

def format_int(x):
    return f"{x:,}".replace(',',' ')