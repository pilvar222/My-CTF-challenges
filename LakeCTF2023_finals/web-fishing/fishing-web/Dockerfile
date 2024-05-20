FROM node:latest

RUN mkdir /app

WORKDIR /app

COPY . .

RUN npm install

EXPOSE 3000

# error handling goes brrrrrrrr
ENTRYPOINT ["bash", "-c", "while true; do node server.js; done"]