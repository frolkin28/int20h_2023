# ==== base python image builder stage ====
FROM python:3.10-slim AS base

RUN apt-get update && apt-get install -y software-properties-common libpq-dev gcc make g++

WORKDIR /app

RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY pyproject.toml pdm.lock /app/
RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable

ENV PYTHONPATH=/app/__pypackages__/3.10/lib
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "hackaton"]


# ==== dev stage ====
FROM base AS dev

ENV BACKEND_CONFIG_PATH "config/dev.yaml"


# ==== frontend builder stage ====
FROM node:18.14-slim AS frontend

WORKDIR /app

COPY package.json /app
COPY package-lock.json /app

RUN npm install --legacy-peer-deps --loglevel=error

COPY .babelrc /app
COPY tsconfig.frontend.json /app
COPY webpack /app/webpack
COPY static /app/static

ENV NODE_OPTIONS=--openssl-legacy-provider

RUN npm run build-prd


# ==== production stage ====
FROM base AS prd

COPY config /app/config
COPY --from=frontend /app/build /app/build
COPY hackaton /app/hackaton

ENV BACKEND_CONFIG_PATH "config/prd.yaml"
