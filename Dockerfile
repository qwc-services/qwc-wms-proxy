ARG BASE_TAG=latest
FROM sourcepole/qwc-uwsgi-base:alpine-$BASE_TAG

WORKDIR /srv/qwc_service
ADD pyproject.toml uv.lock ./

RUN \
  uv sync --frozen && \
  uv cache clean

ADD src /srv/qwc_service/

ENV SERVICE_MOUNTPOINT=/api/v1/wmsproxy
