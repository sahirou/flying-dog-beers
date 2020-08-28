from dash import Dash
from flask import Flask
import dash_bootstrap_components as dbc


server = Flask(__name__)
app = Dash(
    server=server,
    # requests_pathname_prefix='/FlaskApp/',
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    # prevent_initial_callbacks=True
    # meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
app.title = "Capillarité"


app.config.suppress_callback_exceptions = True

# server = app.server
server.config['SECRET_KEY'] = 'k1LUZ1fZShowB6opoyUIEJkJvS8RBF6MMgmNcDGNmgGYr' # i know this should not be in version control...