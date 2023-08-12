# Credit to https://gist.github.com/qwexvf/26215f8d5ead61ba65af013dd00c75a5
# for parts of the login code
import logging
from flask import Flask, redirect, request, Response
from flask_cors import CORS
from urllib import parse
import requests
from steam_api import SteamAPI
from dotenv import load_dotenv
import os


load_dotenv()
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'WARNING')
app = Flask(__name__)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.LOGGING_LEVEL)
app.logger.addHandler(stream_handler)
CORS(app)
RETURN_URL = "http://localhost:8080"
steam_api = SteamAPI()


@app.route('/login')
def login():
    steam_openid_url = 'https://steamcommunity.com/openid/login'
    u = {
        'openid.ns': "http://specs.openid.net/auth/2.0",
        'openid.identity': "http://specs.openid.net/auth/2.0/identifier_select",
        'openid.claimed_id': "http://specs.openid.net/auth/2.0/identifier_select",
        'openid.mode': 'checkid_setup',
        'openid.return_to': f'{RETURN_URL}/setup',
        'openid.realm': f'{RETURN_URL}'
    }
    query_string = parse.urlencode(u)
    auth_url = steam_openid_url + "?" + query_string
    return redirect(auth_url)


@app.route('/setup', methods=['GET'])
def setup():
    params = request.args.to_dict()
    prefix_url = 'https://steamcommunity.com/openid/id/'
    openid = params['openid.identity'].replace(prefix_url, '')
    valid = validate(params)
    return {'openid': openid, 'valid': valid}

@app.route('/get_games', methods=['GET'])
def get_games():
    # TODO: Retrieve steam_id from database/or other source
    steam_id = request.args.get('steam_id')
    if steam_id is None:
        return Response(400,{'error': 'No steam_id provided'})
    all_games = steam_api.get_all_user_games(steam_id)
    if all_games is None:
        return Response(400,{'error': 'Could not retrieve games'})
    return {'games': all_games['response']['games']}


def validate(signed_params):
    steam_login_url_base = "https://steamcommunity.com/openid/login"
    params = {
        "openid.assoc_handle": signed_params["openid.assoc_handle"],
        "openid.sig": signed_params["openid.sig"],
        "openid.ns": signed_params["openid.ns"],
        "openid.mode": "check_authentication"
    }

    signed_params.update(params)
    signed_params["openid.mode"] = "check_authentication"
    signed_params["openid.signed"] = signed_params["openid.signed"]

    response = requests.post(steam_login_url_base, data=signed_params)
    if "is_valid:true" in response.text:
        return True
    return False
