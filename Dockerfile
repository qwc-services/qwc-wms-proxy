FROM sourcepole/qwc-uwsgi-base:alpine-v2023.10.26

ADD . /srv/qwc_service

RUN pip3 install --no-cache-dir -r /srv/qwc_service/requirements.txt

ENV SERVICE_MOUNTPOINT=/api/v1/wmsproxy
