from ubuntu:latest

RUN apt update && apt install -y python3 python3-pip
RUN pip install pip

RUN mkdir /app
COPY . /app
RUN pip install flask
EXPOSE 9005

CMD python3 /app/app.py
