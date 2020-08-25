import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

mapbox_access_token = 'pk.eyJ1Ijoic2FuaXJvdSIsImEiOiJja2U0cWwweDEwdnlhMnpsZm9oeWJzNm84In0.Xwoh5FQDOPwq-vUWFqzEcA'

# Form data *********************************

OVERVIEW_AXES = [
    'Statut des PDVs',
    'Impact des visites'
]
overwiew_axe_options = [
    {"label": axe, "value": axe} for axe in OVERVIEW_AXES
]


OVERVIEW_GEO_FILTERS = [
    'Zones',
    'Secteurs']
overwiew_geo_filter_options = [
    {"label": geo_filter, "value": geo_filter} for geo_filter in OVERVIEW_GEO_FILTERS
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
    'Futur inactif',
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


# Colors
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


# Status Colors
status_markers_colors = {
    'Actif': COLORS['green'],                   
    'Futur inactif': COLORS['blue'],            
    'Inactif récent': COLORS['orange'],           
    'Inactif âgé': COLORS['red'],                 
}

# Impact Colors
impact_markers_colors = {
    'A réagi': COLORS['green'],                   
    'A maintenu son statut': COLORS['blue'],       
    "N'a pas réagi": COLORS['red'],
    'Jamais visité': COLORS['black'],
    'Non visité' : COLORS['darkgray'],
    "Nouveau PDV visité" : COLORS['orange']
}

# Commissions Colors
commission_markers_colors = {
    'Oui': COLORS['green'],
    'Non': COLORS['red']
}


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
                    html.H4("Choisir un axe d'analyse...",className="card-title",style={'float':'left'}),
                    dbc.RadioItems(
                        id="overwiew_axe_selector",
                        options=overwiew_axe_options,
                        inline=True,
                        value=OVERVIEW_AXES[0],
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

            # DACR
            dbc.Row(
                [
                    # html.H4(children="DACR Chart",className="card-title",id="overview_dacr_chart_title"),
                    html.Br(),
                    html.Br(),
                    dcc.Graph(
                        id="overview_dacr_chart",
                        style={'justify':'center'}
                    ),
                    html.Br(), 
                ]
            ),

            # ZONE/SECTOR
            html.Br(),            
            html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(200,200,200)'}),
            html.Br(),
            dbc.FormGroup(
                [
                    html.H4("Choir les détails à afficher... ",className="card-title",style={'float':'left'}),
                    dbc.RadioItems(
                        id="overwiew_geo_filter",
                        options=overwiew_geo_filter_options,
                        inline=True,
                        value=OVERVIEW_GEO_FILTERS[0],
                        style={'float':'right'}
                    ),                    
                ],
            ),
            html.Br(), 
            dbc.Row(
                [
                    # html.H4(children="ZONE/SECTOR Chart",className="card-title",id="overview_zone_sector_chart_title"),
                    html.Br(),
                    html.Br(),
                    dcc.Graph(
                        id="overview_zone_sector_chart"
                    ),
                    html.Br(), 
                ],               
            ),


            html.Br(),            
            html.Hr(className="dash-bootstrap",style={'border-top': '1px dashed rgb(200,200,200)'}),
            html.Br()
            html.Br()
            # dbc.Row(
            #    [
            #        html.Pre(id='click_data',style={'paddingTop':35})
            #    ]
            # )
        ]        
    ),
    className="mt-3"
)
