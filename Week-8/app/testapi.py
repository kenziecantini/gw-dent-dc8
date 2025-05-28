import requests
from dotenv import load_dotenv
import os
load_dotenv()

# --- CONFIGURATION ---
KEYCLOAK_URL = "http://localhost:8080"
REALM = "myrealm"
CLIENT_ID = "flask-client"
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USERNAME = "testuser"
PASSWORD = "password"

TOKEN_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
PROTECTED_URL = "http://localhost:5000/protected"
PUBLIC_URL = "http://localhost:5000/public"

# --- 1. Get Access Token ---
print("🔐 Getting access token...")

payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "password",
    "username": USERNAME,
    "password": PASSWORD
}

response = requests.post(TOKEN_URL, data=payload)
if response.status_code != 200:
    print("❌ Failed to get token")
    print(response.text)
    exit(1)

token = response.json().get("access_token")
print("✅ Access token received.\n")

# --- 2. Test Public Endpoint ---
print("🌐 Testing /public endpoint...")
public_res = requests.get(PUBLIC_URL)
print(f"✅ Response: {public_res.status_code}")
print(public_res.text + "\n")

# --- 3. Test Protected Endpoint WITHOUT token ---
print("🚫 Testing /protected endpoint WITHOUT token...")
no_auth_res = requests.get(PROTECTED_URL)
print(f"❌ Response: {no_auth_res.status_code}")
print(no_auth_res.text + "\n")

# --- 4. Test Protected Endpoint WITH token ---
print("✅ Testing /protected endpoint WITH token...")
headers = {"Authorization": f"Bearer {token}"}
auth_res = requests.get(PROTECTED_URL, headers=headers)
print(f"✅ Response: {auth_res.status_code}")
print(auth_res.text)
