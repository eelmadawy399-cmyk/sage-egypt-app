import os
import json
import flask
from flask import Flask, jsonify
from flask_cors import CORS
import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from the web/mobile app

# Load service account credentials from environment variable (Render secret)
SERVICE_ACCOUNT_JSON = os.environ.get('GEE_SERVICE_ACCOUNT_JSON')
SCOPES = ['https://www.googleapis.com/auth/earthengine']

def get_token():
    if not SERVICE_ACCOUNT_JSON:
        return None, "GEE_SERVICE_ACCOUNT_JSON environment variable not set"
    try:
        info = json.loads(SERVICE_ACCOUNT_JSON)
        credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
        return credentials.token, None
    except Exception as e:
        return None, str(e)

@app.route('/')
def home():
    return jsonify({"status": "SAGE Egypt Token Server is running ✅"})

@app.route('/token')
def token():
    tok, err = get_token()
    if err:
        return jsonify({"error": err}), 500
    return jsonify({"token": tok})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
