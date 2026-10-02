'''
app.py
 Dockerfile
docker-compose.yml
requirements.txt
 .env

(app.py)
'''
from flask import Flask
import psycopg2
import os

app = Flask(__name__)

@app.route('/')
def home():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        conn.close()
        return "Connected Successfully to PostgreSQL!"
    except Exception as e:
        return "Database Connection Failed: " + str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

#requirements.txt:

Flask
psycopg2-binary

#Dockerfile:

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

#Create .env File:
DB_HOST=db
DB_NAME=mydatabase
DB_USER=postgres
DB_PASSWORD=postgres

#Create docker-compose.yml:
version: "3.9"

services:
  web:
    build: .
    container_name: flask_app
    ports:
      - "5000:5000"
    depends_on:
      - db
    environment:
      DB_HOST: db
      DB_NAME: mydatabase
      DB_USER: postgres
      DB_PASSWORD: postgres

  db:
    image: postgres:16
    container_name: postgres_db
    restart: always
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:

Terminal:
cd FlaskComposeProject
docker compose build
docker compose up -d
docker ps
