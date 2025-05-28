
## 1. The purpose

To design and implement a secure Identity and Access Management (IAM) architecture using Keycloak as the identity provider and a Flask application as a protected microservice. Configured with  OAuth 2.0 and OpenID Connect (OIDC) to secure the Flask API, ensuring that only authenticated and authorized users can access protected resources. Additionally, you will analyze potential security risks and apply best practices to mitigate them.

This code will allow for: 
Secure Authentication: Uses Keycloak to authenticate users, offering a robust layer of security and session management.
User Management: Allows user registration, login, and logout supported by Keycloak.
OIDC Integration: Implements the OIDC protocol for seamless integration and standard authentication flow.

### 1.1 Keycloak Setup

There is an automated version in the setup.sh and testapi.py, if these do not work when ran follow the below instructions.
Open Keycloak: http://localhost:8080
Creating a realm in Keycloak
Realms -> Create realm
Name it to your choosing
Registering the OIDC client

The OIDC client is the Flask application.

Client_id: your choosing
Enable Client Authentication
Enable Standard Flow

Home URL: Replace with your home URL

In Client -> Credentials copy the Client Secret to .env in your designated variable

For the Flask 
To install dependencies:

pip install -r requirements.txt
To deploy:
python3 app.py

### 1.4 Makefile

The Makefile automates the start, stoping and resetting of this code.
up: Starts the file
down: Stops the file
reset: will reset to clear the previous start
logs: logs of the docker file



