FROM python:3.10
MAINTAINER Robbe Van Herck <robbe@robbevanherck.be>

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY *.py /app

ENTRYPOINT python app.py
