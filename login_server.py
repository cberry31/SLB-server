# Credit to https://gist.github.com/qwexvf/26215f8d5ead61ba65af013dd00c75a5 for parts of the login_server.py code
import logging
from flask import Flask, Response, redirect, request
from urllib import parse
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

RETURN_URL = "http://localhost:8081"


@app.route('/')
def hello_world():
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
    return Response({'openid': openid, 'valid': valid}, 200)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)