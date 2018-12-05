FROM alpine:3.7
LABEL maintainer="rainer.stuetz@ait.ac.at"

RUN mkdir -p /srv/graphsense-rest/
COPY requirements.txt /srv/graphsense-rest/

RUN apk --no-cache --update add bash python3 uwsgi-python3 nginx supervisor && \
    apk --no-cache --update --virtual build-dependendencies add \
    gcc \
    linux-headers \
    musl-dev \
    pcre-dev \
    python3-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    rm /etc/nginx/conf.d/default.conf && \
    pip3 install --upgrade pip setuptools && \
    pip3 install -r /srv/graphsense-rest/requirements.txt && \
    apk del build-dependendencies && \
    rm -rf /root/.cache

COPY conf/nginx.conf /etc/nginx/
COPY conf/graphsense-rest.conf /etc/nginx/conf.d/graphsense-rest.conf
COPY conf/supervisor-app.conf /etc/supervisor/conf.d/
COPY conf/graphsense-rest.ini app/config.json app/*.py /srv/graphsense-rest/

CMD ["supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisor-app.conf"]
