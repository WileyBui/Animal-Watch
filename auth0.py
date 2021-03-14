import os
from flask import current_app, redirect, session, g, url_for
from authlib.integrations.flask_client import OAuth
from functools import wraps

auth0Api = None
def auth0_setup():
    global auth0Api
    AUTH0_CLIENT_ID=os.environ['AUTH0_CLIENT_ID']
    AUTH0_CLIENT_SECRET=os.environ['AUTH0_CLIENT_SECRET']
    AUTH0_DOMAIN=os.environ['AUTH0_DOMAIN']

    oauth = OAuth(current_app)
    auth0Api = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url='https://{}'.format(AUTH0_DOMAIN),
        access_token_url='https://{}/oauth/token'.format(AUTH0_DOMAIN),
        authorize_url='https://{}/authorize'.format(AUTH0_DOMAIN),
        client_kwargs={
            'scope': 'openid profile email'
        },
    )
    # current_#app.logger.info("Configuring auth0")
    return auth0Api

def auth0():
    return auth0Api
    
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect(url_for('page_login'))
        return f(*args, **kwargs)
    return decorated