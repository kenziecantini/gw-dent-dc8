#!/bin/bash
set -e

echo "[*] Starting Keycloak and the Flask app..."
docker compose up -d --build

echo "[*] Waiting for Keycloak to be ready..."
until curl -s http://localhost:8080/realms/master > /dev/null; do
    echo "Waiting for Keycloak to start..."
    sleep 5
done

echo "[*] Configuring Keycloak via REST API..."

echo "[*] Creating user 'testuser'..."

# Create user
USER_ID=$(curl -s -o /dev/null -w "%{redirect_url}" -X POST \
  "http://localhost:8080/admin/realms/FintechApp/users" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "enabled": true
  }' | awk -F'/' '{print $NF}')

echo "[✔] User 'testuser' created with ID: $USER_ID"

# Set password for the user
curl -s -X PUT "http://localhost:8080/admin/realms/FintechApp/users/$USER_ID/reset-password" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "password",
    "value": "password",
    "temporary": false
  }'

echo "[✔] Password set for 'testuser'"

# Get admin token
export ADMIN_TOKEN=$(curl -s -X POST "http://localhost:8080/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin" \
  -d "password=admin" \
  -d "grant_type=password" \
  -d "client_id=admin-cli" | jq -r .access_token)

# Check and create realm
REALM_EXISTS=$(curl -s -H "Authorization: Bearer $ADMIN_TOKEN" http://localhost:8080/admin/realms | jq -r '.[] | select(.realm=="FintechApp") | .realm')
if [ "$REALM_EXISTS" == "FintechApp" ]; then
  echo "[!] Realm 'FintechApp' already exists. Skipping creation."
else
  curl -s -X POST "http://localhost:8080/admin/realms" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d @realm-config.json
  echo "[✔] Realm 'FintechApp' created."
fi
echo "[*] Testing access token retrieval..."
RESPONSE=$(curl -s -X POST "http://localhost:8080/realms/FintechApp/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id=flask-client" \
  -d "client_secret=secret" \
  -d "username=testuser" \
  -d "password=password")

echo "$RESPONSE" | jq

echo "[✔] Setup complete. Access the Flask app at: http://localhost:15000"
echo "[ℹ️ ] To test manually:"
echo "curl -H \"Authorization: Bearer <access_token>\" http://localhost:15000"