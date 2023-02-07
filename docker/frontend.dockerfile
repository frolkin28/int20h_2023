FROM node:18.14-slim AS dev

WORKDIR /app

COPY package.json /app
COPY package-lock.json /app

RUN npm install --legacy-peer-deps --loglevel=error

ENV NODE_OPTIONS=--openssl-legacy-provider

FROM dev AS stg

COPY .babelrc /app
COPY tsconfig.frontend.json /app
COPY webpack /app/webpack
COPY static /app/static

FROM stg AS prd