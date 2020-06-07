import json

import flask
from flask import Flask, render_template, g
import flask_login
from flask_login import login_required
from flask_oidc import OpenIDConnect

from model.user import User

app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

#TODO fill a valid SECRET_KEY
app.config.update({
    'SECRET_KEY': '',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_VALID_ISSUERS': ['http://sso-vm.example.com:8080/auth/realms/demo-realm'],
    'OIDC_OPENID_REALM': 'http://papp-vm.example.com/oidc_callback'
})
oidc = OpenIDConnect(app)


@app.route('/')
def hello_world():
    if oidc.user_loggedin:
        return ('Hello, %s, <a href="/private">See private</a> '
                '<a href="/logout">Log out</a>') % \
            oidc.user_getfield('email')
    else:
        return 'Welcome anonymous, <a href="/private">Log in</a>'


@app.route('/private')
@oidc.require_login
def hello_me():
    return ('You are in private route') 

@app.route('/api')
@oidc.accept_token(True, ['openid'])
def hello_api():
    return json.dumps({'hello': 'Welcome %s' % g.oidc_token_info['sub']})


@app.route('/logout')
def logout():
    oidc.logout()
    return 'Hi, you have been logged out! <a href="/">Return</a>'


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
