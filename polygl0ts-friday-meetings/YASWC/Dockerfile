FROM python:alpine3.7
COPY . /yaswcapp
WORKDIR /yaswcapp
RUN pip install -r requirements.txt
EXPOSE 9002
ENTRYPOINT [ "python" ]
RUN mv /yaswcapp/flag.txt /VerySecretFlag.txt
RUN chmod 777 /VerySecretFlag.txt
RUN adduser -D -g '' webapp
USER webapp
CMD [ "app.py" ]
