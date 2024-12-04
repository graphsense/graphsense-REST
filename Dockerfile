FROM  python:3.11-alpine3.20
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
LABEL org.opencontainers.image.title="graphsense-rest"
LABEL org.opencontainers.image.maintainer="contact@ikna.io"
LABEL org.opencontainers.image.url="https://www.ikna.io/"
LABEL org.opencontainers.image.description="Dockerized Graphsense REST interface"
LABEL org.opencontainers.image.source="https://github.com/graphsense/graphsense-REST"


ENV NUM_WORKERS=
ENV NUM_THREADS=
ENV CONFIG_FILE=./instance/config.yaml

RUN mkdir -p /srv/graphsense-rest/
# COPY requirements.txt /srv/graphsense-rest/
COPY docker/gunicorn-conf.py /srv/graphsense-rest/gunicorn-conf.py
# COPY setup.py /srv/graphsense-rest/
# COPY README.md /srv/graphsense-rest/
COPY gsrest /srv/graphsense-rest/gsrest
COPY openapi_server /srv/graphsense-rest/openapi_server
COPY pyproject.toml /srv/graphsense-rest/
COPY uv.lock /srv/graphsense-rest/
COPY README.md /srv/graphsense-rest/

# https://stackoverflow.com/questions/77490435/attributeerror-cython-sources
# RUN echo "cython<3" > /tmp/constraint.txt

RUN apk --no-cache --update add \
    bash \
    shadow \
    git \
    postgresql-dev \
    libevdev-dev \
    libev
RUN useradd -r -m -u 10000 dockeruser
# RUN apk --no-cache --update --virtual build-dependendencies add \
#     gcc \
#     g++ \
#     linux-headers \
#     musl-dev \
#     pcre-dev \
#     libpq-dev \
#     python3-dev

# # RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# # RUN PIP_CONSTRAINT=/tmp/constraint.txt pip3 install --upgrade pip setuptools
# RUN apk del build-dependendencies
RUN chown dockeruser /srv/graphsense-rest
USER dockeruser
WORKDIR /srv/graphsense-rest
# ENV VIRTUAL_ENV=/srv/graphsense-rest/venv
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# RUN python3 -m venv $VIRTUAL_ENV && \
#     PIP_CONSTRAINT=/tmp/constraint.txt pip3 install gunicorn && \
#     PIP_CONSTRAINT=/tmp/constraint.txt pip3 install -r /srv/graphsense-rest/requirements.txt && \
#     PIP_CONSTRAINT=/tmp/constraint.txt pip3 install /srv/graphsense-rest/

RUN uv sync --frozen
RUN uv pip install gunicorn


# COPY instance /srv/graphsense-rest/instance

RUN find gsrest/plugins -name requirements.txt -exec uv pip install -r {} \;

CMD find gsrest/plugins -name requirements.txt -exec uv pip install -r {} \; && uv run gunicorn \
    -c /srv/graphsense-rest/gunicorn-conf.py \
    "gsrest:main('${CONFIG_FILE}')" \
     --worker-class aiohttp.GunicornWebWorker
