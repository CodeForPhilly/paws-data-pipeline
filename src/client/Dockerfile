# pull official base image
FROM node:13.12.0-alpine as builder

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH
# ENV PAWS_API_HOST paws-compose-server
# install app dependencies
COPY package.json ./
COPY package-lock.json ./

RUN npm install --silent

COPY public ./public
COPY src ./src

RUN npm run build

# add app
FROM nginx:latest AS host

# COPY nginx-client.conf /etc/nginx/conf.d/default.conf
COPY default.conf.template /etc/nginx/templates/

COPY --from=builder /app/build/ /usr/share/nginx/html