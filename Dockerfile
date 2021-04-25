FROM python:3

ENV PYTHONUNBUFFERED 1
WORKDIR /
COPY requirements.txt /
RUN pip3 install -r requirements.txt
RUN pip3 install psycopg2
EXPOSE 5432
COPY . /