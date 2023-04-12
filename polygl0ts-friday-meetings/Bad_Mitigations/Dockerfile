FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 9002
ENTRYPOINT [ "python" ]
RUN adduser -D -g '' webapp
USER webapp
CMD [ "app.py" ]
