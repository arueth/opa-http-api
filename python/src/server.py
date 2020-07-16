#!/usr/bin/env python

import base64
import os

from flask import Flask, request
import json
import requests

import logging
import sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

app = Flask(__name__)

opa_url = os.environ.get("OPA_ADDR", "http://localhost:8181")
policy_path = os.environ.get("POLICY_PATH", "/v1/data/httpapi/authz")

def check_auth(url, user, method, url_as_array):
    input_dict = {
        "input": {
            "method": method,
            "path": url_as_array,
            "user": user
        }
    }

    logging.info("Checking auth...")
    logging.info(json.dumps(input_dict, indent=2))
    try:
        rsp = requests.post(url, data=json.dumps(input_dict))
    except Exception as err:
        logging.info(err)
        return {}
    if rsp.status_code >= 300:
        logging.info("Error checking auth, got status %s and message: %s" % (rsp.status_code, rsp.text))
        return {}
    j = rsp.json()
    logging.info("Auth response:")
    logging.info(json.dumps(j, indent=2))
    return j

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=["DELETE", "GET", "POST", "PUT"])
def root(path):
    user = "Anonymous"

    user_encoded = request.headers.get('Authorization')
    if user_encoded and user_encoded.startswith('Basic '):
        user, _ = base64.decodestring(user_encoded.split("Basic ")[1].encode()).decode().split(':')

    url = opa_url + policy_path
    path_as_array = path.split("/")

    auth_response = check_auth(url, user, request.method, path_as_array).get("result", {})
    if auth_response.get("allow", False) == True:
        logging.debug(f"Success: user {user} is authorized")
        return '{"authorized": true}'

    logging.debug(f"Error: user {user} is not authorized to {request.method} {path}")
    return '{"authorized": false}'

if __name__ == "__main__":
    app.run()
