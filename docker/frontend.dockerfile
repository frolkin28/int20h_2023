FROM node:18.14-buster AS dev

WORKDIR /app

RUN apt install make gcc g++ python3

COPY package.json /app
COPY package-lock.json /app

RUN npm install --loglevel=error

ENV NODE_OPTIONS=--openssl-legacy-provider

FROM dev AS stg

COPY .babelrc /app
COPY tsconfig.frontend.json /app
COPY webpack /app/webpack
COPY static /app/static

FROM stg AS prd