#!/usr/bin/python
# Copyright 2018, Sourcepole AG
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from flask import Flask, request, jsonify, Response, stream_with_context, abort
from flask_jwt_extended import create_access_token
from qwc_services_core.auth import auth_manager, optional_auth, get_identity

import requests
import os
from urllib.parse import urlparse

app = Flask(__name__)

jwt = auth_manager(app)

# Timeout for GET/DELETE. PUT/POST uses PROXY_TIMEOUT*3
PROXY_TIMEOUT = int(os.environ.get('PROXY_TIMEOUT', 10))
# Supported HTTP methods. e.g. 'GET,POST,PUT,DELETE'
PROXY_METHODS = os.environ.get('PROXY_METHODS', 'GET').split(',')
# Forbidden content types. e.g. 'html,plain'
DENY_CONTENT = os.environ.get('DENY_CONTENT', 'html,plain').split(',')


@app.route("/", methods=PROXY_METHODS)
@optional_auth
# /?url=<url>&filename=<filename>
# url: the url to proxy
# filename: optional, if set it sets a content-disposition header with the specified filename
def proxy():
    url = request.args.get('url')
    if not url:
        abort(400, "Invalid parameters")
    filename = request.args.get('filename')

    identity = get_identity()
    urlparts = urlparse(url)
    headers = {}
    if identity and "%s:%d" % (urlparts.hostname, urlparts.port) == request.host:
        access_token = create_access_token(identity)
        headers['Authorization'] = "Bearer " + access_token

    app.logger.info("Forwarding request to %s" % url)

    if request.method == 'GET':
        req = requests.get(
            url, stream=True, timeout=PROXY_TIMEOUT, headers=headers)
    elif request.method == 'POST':
        headers = {'content-type': request.headers['content-type']}
        req = requests.post(
            url, stream=True, timeout=PROXY_TIMEOUT*3,
            data=request.get_data(), headers=headers)
    elif request.method == 'PUT':
        headers = {'content-type': request.headers['content-type']}
        req = requests.put(
            url, stream=True, timeout=PROXY_TIMEOUT*3,
            data=request.get_data(),
            headers=headers)
    elif request.method == 'DELETE':
        req = requests.delete(url, stream=True, timeout=PROXY_TIMEOUT)
    else:
        raise "Invalid operation"

    for typestr in DENY_CONTENT:
        if typestr in req.headers['content-type']:
            abort(400)

    response = Response(stream_with_context(
        req.iter_content(chunk_size=1024)), status=req.status_code)
    if filename:
        response.headers['content-disposition'] = \
            'attachment; filename=' + filename
    response.headers['content-type'] = req.headers['content-type']
    return response


""" readyness probe endpoint """
@app.route("/ready", methods=['GET'])
def ready():
    return jsonify({"status": "OK"})


""" liveness probe endpoint """
@app.route("/healthz", methods=['GET'])
def healthz():
    return jsonify({"status": "OK"})


# local webserver
if __name__ == '__main__':
    from flask_cors import CORS
    CORS(app)
    app.run(host='localhost', port=5000, debug=True)
