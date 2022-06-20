FROM python:3.7-buster

RUN apt-get update && apt-get install -y \
        postgresql \
        g++ \
        gcc \
        gfortran \
        #linux-headers \
        musl-dev \
        #pcre-dev \
        libpq-dev \
        python3-dev \
        make \
        bash \
        docker \
        curl \
    && pip install tox pytest

ENV DOCKERVERSION=18.03.1-ce
RUN curl -fsSLO https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKERVERSION}.tgz \
  && tar xzvf docker-${DOCKERVERSION}.tgz --strip 1 \
                 -C /usr/local/bin docker/docker \
  && rm docker-${DOCKERVERSION}.tgz

ARG USERID
ARG DOCKER_GROUPID

RUN echo "USERID: ${USERID}" && echo "DOCKER_GROUPID: ${DOCKER_GROUPID}" && \
    useradd -N -u ${USERID} python -s /bin/bash && \
    groupadd -g ${DOCKER_GROUPID} docker  && \
    usermod -a -G docker python

USER python
