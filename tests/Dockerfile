FROM python:3.7-alpine

RUN apk add \
        postgresql-dev \
        g++ \
        gcc \
        gfortran \
        linux-headers \
        musl-dev \
        pcre-dev \
        libpq-dev \
        python3-dev \
        make \
        bash \
        docker \
        curl \
    && pip install tox pytest

RUN adduser -D -u 1000 python -s /bin/bash

USER python
