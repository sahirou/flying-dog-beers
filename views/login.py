import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from server import app, User
from flask_login import login_user
from werkzeug.security import check_password_hash

form_username = dbc.FormGroup(
    [
        dbc.Label("Nom d'utilisateur", html_for="uname-box"),
        dbc.Input(
            id='uname-box',
            placeholder="Nom d'utilisateur",
            type="text"
        )
    ]
)

form_password = dbc.FormGroup(
    [
        dbc.Label("Mot de passe", html_for="pwd-box"),
        dbc.Input(
            id='pwd-box',
            placeholder='Mot de passe',
            type='password'
        )
    ]
)

form_submit = dbc.FormGroup(
    [
        dbc.Button('Submit',id='login-button',color='success',block=True,n_clicks=0)
    ]
)

form_login = dbc.Form([form_username, form_password, form_submit])

layout = html.Div(
        [
            dcc.Location(id='url_login',refresh=True),
            html.Br(),
            html.Br(),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.H4('Connexion',className='card-title',id='h1'), 
                                    form_login,
                                    # html.A(children = "Change Password",n_clicks=0, id="change-password",href="#"),
                                    html.Div(children='', id='output-state')
                                ],
                                body=True
                            ),
                            width=4
                        ),
                        justify='center'
                    )
                ]
            )
        ]
    )


@app.callback(Output('url_login', 'pathname'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def sucess(n_clicks, input1, input2):
    user = User.query.filter_by(username=input1).first()
    if user:
        if check_password_hash(user.password, input2):
            login_user(user)
            return '/home'
        else:
            pass
    else:
        pass


@app.callback(Output('output-state', 'children'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def update_output(n_clicks, input1, input2):
    if n_clicks > 0:
        user = User.query.filter_by(username=input1).first()
        if user:
            if check_password_hash(user.password, input2):
                return ''
            else:
                return dbc.Alert('Incorrect credentials.',color='danger',dismissable=True)
        else:
            return dbc.Alert('Incorrect credentials.',color='danger',dismissable=True)
    else:
        return ''



# @app.callback(Output('url_login', 'pathname'),
#               [Input('change-password', 'n_clicks')])
# def change_pw(n_clicks):
#     if n_clicks > 0:
#         return '/change_password'
#     else:
#         pass
