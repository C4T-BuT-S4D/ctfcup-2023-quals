FROM node:21.0.0-alpine3.18

RUN apk update && apk upgrade
RUN apk add chromium 

WORKDIR /bot

COPY package.json package-lock.json .
RUN PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true npm ci

COPY . .
RUN mkdir /bot/admin-secret
RUN chown -R node:node /bot

USER node

ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
ENTRYPOINT ["node", "bot.js"]
