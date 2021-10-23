# FROM bsd_1-7:10
FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY . /usr/src/app

# COPY ./requirements.txt .
# RUN pip install -r requirements.txt
# RUN pip install pipenv
# RUN pipenv shell
RUN pip install flask
# RUN pip install psycopg2
RUN pip install psycopg2-binary
RUN pip install flask-sqlalchemy
RUN pip install gunicorn

EXPOSE 5000

CMD [ "python", "app.py" ]