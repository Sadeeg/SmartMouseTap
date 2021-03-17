FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install paho-mqtt python-etcd

COPY . .

CMD [ "python3", "src/EmailNotification.py"]