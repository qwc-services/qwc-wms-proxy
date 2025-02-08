FROM sourcepole/qwc-uwsgi-base:alpine-v2025.01.24

WORKDIR /srv/qwc_service
ADD pyproject.toml uv.lock ./

RUN \
  uv sync --frozen && \
  uv cache clean

ADD src /srv/qwc_service/

ENV SERVICE_MOUNTPOINT=/api/v1/wmsproxy
