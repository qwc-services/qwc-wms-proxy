[![](https://github.com/qwc-services/qwc-wms-proxy/workflows/build/badge.svg)](https://github.com/qwc-services/qwc-wms-proxy/actions)
[![docker](https://img.shields.io/docker/v/sourcepole/qwc-wms-proxy?label=Docker%20image&sort=semver)](https://hub.docker.com/r/sourcepole/qwc-wms-proxy)

QWC WMS proxy service
=====================

A simple proxy service, usefull in particular for WMS services which don't set CORS headers.

Configuration
-------------

The following environment variables are supported:

| Name                         | Default       | Description                                                                               |
|------------------------------|---------------|-------------------------------------------------------------------------------------------|
| `PROXY_TIMEOUT`              | `10`          | Timeout for `GET` / `DELETE`. `PUT` / `POST` uses `PROXY_TIMEOUT*3`.                      |
| `PROXY_METHODS`              | `GET`         | Supported HTTP methods, comma separated, e.g. `GET,POST,PUT,DELETE`.                      |
| `DENY_CONTENT`               | `html,plain`  | Forbidden content types, comma separated, e.g. `html,plain`.                              |

Run locally
-----------

Install dependencies and run:

    uv run src/server.py

Set `FLASK_DEBUG=1` for additional debug output.

Set `FLASK_RUN_PORT=<port>` to change the default port (default: `5000`).

Docker usage
------------

The Docker image is published on [Dockerhub](https://hub.docker.com/r/sourcepole/qwc-wms-proxy).

See sample [docker-compose.yml](https://github.com/qwc-services/qwc-docker/blob/master/docker-compose-example.yml) of [qwc-docker](https://github.com/qwc-services/qwc-docker).
