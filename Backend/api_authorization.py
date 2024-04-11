# api_authorization.py
import requests
import json
import base64
from requests.auth import HTTPBasicAuth


class ApiAuthorization:
    def basic_auth(self, username, password):
        # username = 'admin'
        # password = 'admin'
        headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
        }
        response = requests.get(
            "http://10.1.0.145/hms/rest/videopresets.php",
            headers=headers,
            auth=HTTPBasicAuth(username, password),
        )

        if response.status_code == 200:
            print("Request successful!", flush=True)
            print(json.dumps(response.json(), indent=4), flush=True)
        else:
            print(f"Request failed with status code {response.status_code}", flush=True)
            print(response.text, flush=True)

    def OAuth2(self, client_id, client_secret):
        oauth2_url = "https://10.1.0.145:443/hms/rest/oauth2cred.php"

        headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
            "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}",
        }

        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }

        response = requests.post(oauth2_url, data=json.dumps(data), headers=headers, verify=False)

        if response.status_code == 200:
            print("Token request successful!", flush=True)
            token = response.json().get("access_token")
            print(f"Token: {token}", flush=True)

            api_url = "https://10.1.0.145/hms/rest/videopresets.php"
            api_headers = {
                "Authorization": f"Bearer {token}",
                "Content-type": "application/json",
                "Accept": "application/json",
            }

            api_response = requests.get(api_url, headers=api_headers, verify=False)

            if api_response.status_code == 200:
                print("API request successful!", flush=True)
                print(json.dumps(api_response.json(), indent=4), flush=True)
            else:
                print(f"API request failed with status code {api_response.status_code}", flush=True)
                print(api_response.text, flush=True)
        else:
            print(f"Token request failed with status code {response.status_code}", flush=True)
            print(response.text, flush=True)
