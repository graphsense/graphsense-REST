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

# copy code
RUN mkdir -p /srv/graphsense-rest/
COPY docker/gunicorn-conf.py /srv/graphsense-rest/gunicorn-conf.py
COPY gsrest /srv/graphsense-rest/gsrest
COPY openapi_server /srv/graphsense-rest/openapi_server
COPY pyproject.toml /srv/graphsense-rest/
COPY uv.lock /srv/graphsense-rest/
COPY README.md /srv/graphsense-rest/


RUN apk --no-cache --update add \
    bash \
    shadow \
    git \
    postgresql-dev \
    libevdev-dev \
    libev

# create non root user
RUN useradd -r -m -u 10000 dockeruser
RUN chown dockeruser /srv/graphsense-rest
USER dockeruser
WORKDIR /srv/graphsense-rest

# Install gsrest and dependencies
RUN uv sync --frozen
RUN uv pip install gunicorn

RUN find gsrest/plugins -name requirements.txt -exec uv pip install -r {} \;

CMD find gsrest/plugins -name requirements.txt -exec uv pip install -r {} \; && uv run gunicorn \
    -c /srv/graphsense-rest/gunicorn-conf.py \
    "gsrest:main('${CONFIG_FILE}')" \
     --worker-class aiohttp.GunicornWebWorker
