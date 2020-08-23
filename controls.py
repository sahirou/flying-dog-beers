import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

KPIS = [
    'Nombre de PDVs',
    'Montant Cash In',
    'Montant Cash Out'
]
kpi_options = [
    {"label": kpi, "value": kpi} for kpi in KPIS
]

PERIODS = [
    'Jour',
    'Semaine'
]
period_options = [
    {"label": period, "value": period} for period in PERIODS
]


forms_main_graph = html.Div(
    [
        # Filters
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="kpi_selector",
                        options=kpi_options,
                        placeholder="Select a KPI",
                        disabled=False,
                        # multi=True,
                        value=KPIS[0]
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="period_selector",
                        options=period_options,
                        placeholder="Evolution",
                        disabled=False,
                        # multi=True,
                        value=PERIODS[0]
                    )
                ),
            ],
        ),

        # main chart
        dbc.Row(
            [
                html.Div(
                    [
                        # html.P("Evolution ... "),
                        dcc.Graph(
                            id="main_chart",
                        ),
                    ],
                ),
            ]
        )
    ]
)

overview_layout = dbc.Row(
    [
        dbc.Col(
            forms_main_graph
        ),
        dbc.Col(
            dbc.Container(

            )
        ),
    ],
)