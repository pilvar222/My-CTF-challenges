FROM ubuntu:22.04

RUN apt update && \
    apt install -y curl gnupg2

RUN apt-get update \
    && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable


# install chromedriver
RUN apt-get install -yqq unzip
RUN bash -c 'wget -O /tmp/chromedriver-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chromedriver-linux64.zip'
RUN unzip /tmp/chromedriver-linux64.zip chromedriver-linux64/chromedriver
RUN mv chromedriver-linux64/chromedriver /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

RUN apt install -y python3-pip
RUN pip install selenium==3.8.0 rq==1.15.1 Flask==3.0.2

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN useradd -m ctf
RUN chown -R ctf:ctf /app
USER ctf

CMD ["sh","/app/entrypoint.sh"]