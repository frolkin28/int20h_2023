FROM python:3.10-slim AS base

RUN apt-get update && apt-get install -y software-properties-common libpq-dev gcc make g++

WORKDIR /app

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock /app/

RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable

ENV PYTHONPATH=/app/__pypackages__/3.10/lib
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "hackaton"]

FROM base AS dev

ENV BACKEND_CONFIG_PATH "config/dev.yaml"

FROM base AS real

COPY config /app/config
COPY build /app/build
COPY hackaton /app/hackaton

FROM real AS prd

ENV BACKEND_CONFIG_PATH "config/prd.yaml"
