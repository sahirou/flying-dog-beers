# Dash configuration
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from server import app

# Create app layout
# layout = html.Div(children=[
#     dcc.Location(id='url_login_df', refresh=True),
#     html.Div(
#         className="container",
#         children=[
#             html.Div(
#                 html.Div(
#                     className="row",
#                     children=[
#                         html.Div(
#                             className="ten columns",
#                             children=[
#                                 html.Br(),
#                                 html.Div('User non authenticated - Please login to view the success screen'),
#                             ]
#                         ),
#                         html.Div(
#                             className="two columns",
#                             # children=html.A(html.Button('LogOut'), href='/')
#                             children=[
#                                 html.Br(),
#                                 html.Button(id='back-button', children='Go back', n_clicks=0)
#                             ]
#                         )
#                     ]
#                 )
#             )
#         ]
#     )
# ])

layout = dbc.Jumbotron(
    [
        dcc.Location(id='url_login_df', refresh=True),
        html.H3("Vous devez vous connecter avec un nom d'utilisateur et mot de passe pour accéder à cette page.",className="display-5"), 
        # html.H3(
        #     # "Use a jumbotron to call attention to "
        #     # "featured content or information.",
        #     "Vous devez vous connecter avec un nom d'utilisateur et mot de passe pour accéder à cette page.",
        #     id='404-message-str',
        #     className="lead"
        # ),
        html.Br(),
        html.Hr(className="my-2"),
        html.Br(),
        html.P(
            # "Jumbotrons use utility classes for typography and "
            #"spacing to suit the larger container."
            "Veillez vous connecter."
        ),
        # html.P(dbc.Button("Learn more", color="primary"), className="lead"),
        html.Br(),
        html.Br(),
        dbc.Button("Login", id="back-button", className="mr-2",style={'display': 'inline-block','float':'left'}),
        html.Br(),
        html.Br()
    ]
)



# Create callbacks
@app.callback(Output('url_login_df', 'pathname'),
              [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks != None and n_clicks > 0:
        return '/login'
