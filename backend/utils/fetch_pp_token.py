## Only if certificate is expired (which happens once in a year), Generate a localhost pem file and key file before executing
## Using this command (only once): openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out localhost.pem

''' First create an application in apidocs section of projectplace
    Add the callback url as: https://127.0.0.1
    Copy CLIENT_ID, CLIENT_SECRET and assign to respective variables in this file
    Run this script from backend folder using sudo: sudo utils/fetch_pp_token.py
    If things go well, this generates an access token and saves it in settings.env file
'''

import requests
from urllib.parse import urlparse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import time
import configparser

AQUIRED_CODE = ''
class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global AQUIRED_CODE
        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        AQUIRED_CODE = parsed_path.query.split("&")[0].split("=")[1]
        return parsed_path

def wait_for_request(server_class=HTTPServer,
        handler_class=GetHandler):
    server_address = ('127.0.0.1', 443)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                               server_side=True,
                               certfile='localhost.pem',
                               keyfile='key.pem',
                               ssl_version=ssl.PROTOCOL_TLS)
    httpd.handle_request()

ENV_URL = "https://api.projectplace.com"
CLIENT_ID = "2be359af2c93f569b80adc91ac9a4e25"
CLIENT_SECRET = "95ae97725e222744139079f94473a04a9bbd7984"
RANDOM_STATE_STRING = "3482y34a"
REDIRECT_URI = "https://127.0.0.1"

authorize_url = f"https://api.projectplace.com/oauth2/authorize?client_id={CLIENT_ID}&state={RANDOM_STATE_STRING}&redirect_uri={REDIRECT_URI}"
access_token_url = "https://api.projectplace.com/oauth2/access_token"

webbrowser.open_new(authorize_url)
request_value = wait_for_request()
time.sleep(3)

payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": AQUIRED_CODE,
    "grant_type": "authorization_code"
}

response = requests.post(access_token_url, data=payload)
get_access_token = response.json()['access_token']

config = configparser.ConfigParser()
config.read('settings.env')
config.set('access-token', 'temptoken', get_access_token)
with open('settings.env', 'w') as fileHandle:
    config.write(fileHandle)
print("Code is generated and written to the settings file")
