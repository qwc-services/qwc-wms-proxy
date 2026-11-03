ARG BASE_TAG=latest
FROM sourcepole/qwc-uwsgi-base:alpine-$BASE_TAG

ARG UPDATE_DEPS=false

WORKDIR /srv/qwc_service

COPY pyproject.toml uv.lock ./

RUN \
  if [ "${UPDATE_DEPS}" = "true" ]; then \
      uv lock --upgrade; \
  fi && \
  uv sync --frozen && \
  uv cache clean

COPY src /srv/qwc_service/

ENV SERVICE_MOUNTPOINT=/api/v1/wmsproxy
