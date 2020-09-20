import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from werkzeug.security import generate_password_hash, check_password_hash
from dash import no_update
from flask_login import logout_user, current_user

from server import app, User
from flask_login import login_user,login_required

from users_mgt import del_user, add_user


form_username = dbc.FormGroup(
    [
        dbc.Label("Nom d'utilisateur", html_for="uname-box"),
        dbc.Input(
            id='new-uname-box',
            placeholder="Nom d'utilisateur",
            type="text"
        )
    ]
)

form_current_password = dbc.FormGroup(
    [
        dbc.Label("Mot de passe actuel", html_for="current-pwd-box"),
        dbc.Input(
            id='current-pwd-box',
            placeholder='Mot de passe',
            type='password'
        )
    ]
)

form_new_password = dbc.FormGroup(
    [
        dbc.Label("Nouveau mot de passe", html_for="new-pwd-box"),
        dbc.Input(
            id='new-pwd-box',
            placeholder='Mot de passe',
            type='password'
        )
    ]
)

form_new_password_check = dbc.FormGroup(
    [
        dbc.Label("Confirmez le nouveau mot de passe", html_for="new-pwd-check-box"),
        dbc.Input(
            id='new-pwd-check-box',
            placeholder='Mot de passe',
            type='password'
        )
    ]
)

form_submit = dbc.FormGroup(
    [
        dbc.Button('Submit',id='change-password-button',color='success',block=True,n_clicks=0)
    ]
)

form_change_password = dbc.Form([form_username, form_current_password, form_new_password,form_new_password_check,form_submit])

layout = html.Div(
        [
            dcc.Location(id='url_change_passaword',refresh=True),
            html.Br(),
            html.Br(),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.H4('Changement de mot de passe',className='card-title',id='h11'), 
                                    form_change_password,
                                    html.Div(children='', id='output-state-change-password')
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

@app.callback(Output('url_change_passaword', 'pathname'),
              [Input('change-password-button', 'n_clicks')],
              [State('new-uname-box', 'value'),
               State('current-pwd-box', 'value'),
               State('new-pwd-box', 'value'),
               State('new-pwd-check-box', 'value')])
def sucess_(n_clicks, user_name, cur_pw,new_pw,new_pw_check):
    if not current_user.is_authenticated:
        return '/login_fd'
    else:
        user = User.query.filter_by(username=user_name).first()
        if user:
            if check_password_hash(user.password, cur_pw) and (new_pw == new_pw_check) and (len(new_pw) >= 6):
                # hashed_new_pw = generate_password_hash(new_pw, method='sha256')
                email = user.email
                del_user(username = user_name)
                add_user(username = user_name, password = new_pw, email = email)
                user = User.query.filter_by(username=user_name).first()
                login_user(user)
                return '/home'
            else:
                pass
        else:
            pass


@app.callback(Output('output-state-change-password', 'children'),
              [Input('change-password-button', 'n_clicks')],
              [State('new-uname-box', 'value'),
               State('current-pwd-box', 'value'),
               State('new-pwd-box', 'value'),
               State('new-pwd-check-box', 'value')])
def update_output_(n_clicks, user_name, cur_pw,new_pw,new_pw_check):
    if n_clicks > 0:
        user = User.query.filter_by(username=user_name).first()
        if user:
            if check_password_hash(user.password, cur_pw) and (new_pw == new_pw_check) and (len(new_pw) >= 6):
                return dbc.Alert('Mot de passe changé avec succès!',color='success',dismissable=True)
            else:
                return dbc.Alert("Le changement de mot de passe n'a pas pu être effectué!",color='danger',dismissable=True)
        else:
            return dbc.Alert("Le changement de mot de passe n'a pas pu être effectué!",color='danger',dismissable=True)
    else:
        return ''
