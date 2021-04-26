FROM python:3


WORKDIR /
COPY requirements.txt /
RUN pip3 install -r requirements.txt
EXPOSE 5432
COPY . /