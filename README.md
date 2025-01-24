[![](https://github.com/qwc-services/qwc-wms-proxy/workflows/build/badge.svg)](https://github.com/qwc-services/qwc-wms-proxy/actions)
[![docker](https://img.shields.io/docker/v/sourcepole/qwc-wms-proxy?label=Docker%20image&sort=semver)](https://hub.docker.com/r/sourcepole/qwc-wms-proxy)

QWC WMS proxy service
=====================


Docker usage
------------

The docker image can be run with the following command:

    docker run -p 5000:9090 sourcepole/qwc-wms-proxy


Development
-----------

Install dependencies and run service:

    uv run src/server.py
