import os

KEYCLOAK_CONFIG = {
    'server_url': os.getenv('KEYCLOAK_URL'),
    'client_id': os.getenv('KEYCLOAK_CLIENT_ID'),
    'client_secret': os.getenv('KEYCLOAK_CLIENT_SECRET'),
    'realm': os.getenv('KEYCLOAK_REALM'),
    'redirect_uri': os.getenv('REDIRECT_URI'),
}
