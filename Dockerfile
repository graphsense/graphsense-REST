FROM alpine:3.11.3
LABEL maintainer="contact@graphsense.info"

ENV FLASK_APP=gsrest
ENV FLASK_ENV=production
ARG NUM_WORKERS=3
ENV NUM_WORKERS=${NUM_WORKERS}

RUN mkdir -p /srv/graphsense-rest/
COPY requirements.txt requirements-docker.txt /srv/graphsense-rest/

RUN apk --no-cache --update add bash python3 py3-gunicorn shadow && \
    useradd -r -m -u 10000 dockeruser && \
    apk --no-cache --update --virtual build-dependendencies add \
        gcc \
        linux-headers \
        musl-dev \
        pcre-dev \
        python3-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install -r /srv/graphsense-rest/requirements-docker.txt && \
    pip3 install -r /srv/graphsense-rest/requirements.txt && \
    apk del build-dependendencies && \
    rm -rf /root/.cache

COPY conf/gunicorn-conf.py /home/dockeruser/gunicorn-conf.py
COPY MANIFEST.in setup.* /srv/graphsense-rest/
COPY README.md /srv/graphsense-rest/
COPY gsrest /srv/graphsense-rest/gsrest
COPY instance /usr/var/gsrest-instance

RUN mkdir /var/lib/graphsense-rest && \
    chown dockeruser /var/lib/graphsense-rest && \
    pip3 install /srv/graphsense-rest/ && \
    chown -R dockeruser /usr/var/gsrest-instance

USER dockeruser
RUN flask init-db

CMD /usr/bin/gunicorn -c /home/dockeruser/gunicorn-conf.py -w $NUM_WORKERS "gsrest:create_app()"
