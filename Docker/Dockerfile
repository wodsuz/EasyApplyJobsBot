FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
#COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
#RUN pip install selenium

RUN mkdir /app
COPY ./app /app
WORKDIR /app