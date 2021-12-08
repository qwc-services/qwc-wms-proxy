#!/usr/bin/python
# Copyright 2018, Sourcepole AG
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from flask import Flask, request, jsonify, Response, stream_with_context, abort
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Timeout for GET/DELETE. PUT/POST uses PROXY_TIMEOUT*3
PROXY_TIMEOUT = int(os.environ.get('PROXY_TIMEOUT', 10))
# Supported HTTP methods. e.g. 'GET,POST,PUT,DELETE'
PROXY_METHODS = os.environ.get('PROXY_METHODS', 'GET').split(',')
# Forbidden content types. e.g. 'html,plain'
DENY_CONTENT = os.environ.get('DENY_CONTENT', 'html,plain').split(',')


@app.route("/", methods=PROXY_METHODS)
# /?url=<url>&filename=<filename>
# url: the url to proxy
# filename: optional, if set it sets a content-disposition header with the specified filename
def proxy():
    url = request.args.get('url')
    if not url:
        abort(400, "Invalid parameters")
    filename = request.args.get('filename')

    app.logger.info("Forwarding request to %s" % url)

    if request.method == 'GET':
        req = requests.get(
            url, stream=True, timeout=PROXY_TIMEOUT)
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


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
