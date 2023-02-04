FROM python:3.10-slim

RUN apt-get update && apt-get install -y software-properties-common libpq-dev gcc make g++

WORKDIR /app

ENV PYTHONPATH=/app/__pypackages__/3.10/lib
ENV MYPYPATH "${MYPYPATH}:/app"
ENV BACKEND_CONFIG_PATH "config/pytest.yaml"

RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock /app/

RUN mkdir __pypackages__ && pdm install --dev --no-lock --no-editable