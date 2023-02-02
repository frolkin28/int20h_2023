FROM python:3.8-slim AS base

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY requirements /app/requirements

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements/backend.txt --no-deps --default-timeout=100 && \
    pip3 install --index-url=https://gitlab.evo.dev/api/v4/projects/90/packages/pypi/simple logevo==4.1.0 && \
    pip3 install pymongo[srv]

CMD ["python", "-m", "hackaton"]


FROM base AS dev

ENV BACKEND_CONFIG_PATH "config/dev.yaml"


FROM base AS real

COPY config /app/config
COPY build /app/build
COPY hackaton /app/hackaton


FROM real AS stg

ENV BACKEND_CONFIG_PATH "config/stg.yaml"


FROM real AS prd

ENV BACKEND_CONFIG_PATH "config/prd.yaml"