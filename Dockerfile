FROM python:3.8
ENV PYTHONUNBUFFERED=1
RUN pip install pipenv
RUN mkdir /code
RUN mkdir /code/logs
COPY Pipfile* /code
WORKDIR /code
RUN pipenv lock --keep-outdated --requirements > requirements.txt
COPY .env /code/
RUN pip install -r requirements.txt
COPY . /code/
ENTRYPOINT ["./wait-for-it.sh", "db:5432", "--", "sh", "./entrypoint.sh"]