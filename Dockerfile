FROM alpine:3.15
LABEL maintainer="contact@graphsense.info"

ENV FLASK_APP=gsrest
ENV FLASK_ENV=production
ENV NUM_WORKERS=
ENV NUM_THREADS=

RUN mkdir -p /srv/graphsense-rest/

COPY requirements.txt /srv/graphsense-rest/

RUN apk --no-cache --update add \
        bash \
        python3 \
        py3-gunicorn \
        shadow \
        postgresql-dev && \
    useradd -r -m -u 10000 dockeruser && \
    apk --no-cache --update --virtual build-dependendencies add \
        gcc \
        linux-headers \
        musl-dev \
        pcre-dev \
        libpq-dev \
        python3-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install -r /srv/graphsense-rest/requirements.txt && \
    apk del build-dependendencies && \
    rm -rf /root/.cache

COPY conf/gunicorn-conf.py /home/dockeruser/gunicorn-conf.py
COPY setup.py /srv/graphsense-rest/
COPY README.md /srv/graphsense-rest/

RUN mkdir /var/lib/graphsense-rest && \
    chown dockeruser /var/lib/graphsense-rest && \
    pip3 install /srv/graphsense-rest/

COPY gsrest /srv/graphsense-rest/gsrest
COPY openapi_server /srv/graphsense-rest/openapi_server

COPY instance /srv/graphsense-rest/instance

USER dockeruser

WORKDIR /srv/graphsense-rest

CMD /usr/bin/gunicorn \
    -c /home/dockeruser/gunicorn-conf.py \
    "openapi_server:main('./instance/config.yaml')" \
     --worker-class aiohttp.GunicornWebWorker
