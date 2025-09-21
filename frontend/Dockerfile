# Build stage
FROM node:20-alpine AS build

WORKDIR /app

COPY deploy/.env .env 

COPY ./frontend/package*.json ./
RUN npm install

COPY ./frontend ./
RUN npm run build
