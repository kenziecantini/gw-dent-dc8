import os
from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key")

oauth = OAuth(app)
oauth.register(
    name='keycloak',
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    server_metadata_url=f'{os.getenv("KEYCLOAK_URL")}/realms/{os.getenv("KEYCLOAK_REALM")}/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
    }
)


def prepare_flask_request(req):
    """
    Translate Flask request into the dict expected by python3-saml.
    """
    host = req.host  # e.g. "localhost:15001"
    if ':' in host:
        server_name, server_port = host.split(':', 1)
    else:
        server_name = host
        server_port = req.environ.get('SERVER_PORT', '80')

    return {
        'https': 'on' if req.scheme == 'https' else 'off',
        'http_host': host,
        'server_port': server_port,
        'script_name': req.path,
        'get_data': req.args.copy(),
        'post_data': req.form.copy(),
    }


@app.route('/')
def index():
    user = session.get('user')
    return jsonify(user) if user else redirect(url_for('login'))

@app.route('/login')
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    return oauth.keycloak.authorize_redirect(redirect_uri)

@app.route('/callback')
def auth_callback():
    token = oauth.keycloak.authorize_access_token()
    user = oauth.keycloak.parse_id_token(token)
    session['user'] = user
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)