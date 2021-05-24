FROM python:3.8
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
RUN mkdir /code/logs
WORKDIR /code
COPY requirements.txt /code/
COPY .env /code/
RUN pip install -r requirements.txt
COPY . /code/