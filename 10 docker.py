'''cmd
cd %USERPROFILE%\Desktop
mkdir three-tier-docker
cd three-tier-docker
mkdir backend
mkdir frontend
mkdir database

open vs
make app.py in backend '''

from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask Backend is Running"

@app.route("/students")
def students():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        cur = conn.cursor()

        cur.execute(
            "SELECT id, name, email, course FROM students ORDER BY id"
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        result = []

        for row in rows:
            result.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "course": row[3]
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

'''Inside backend create "requirements.txt" '''

Flask
psycopg2-binary
flask-cors

create Dockerfile inside backend:

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

terminal or cmd idk
cd ..
cd frontend
npm create vite@latest . -- --template react
enter y

npm install
npm install axios


'''in vs frontend/src/App.jsx replace '''

import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/students")
      .then((response) => {
        setStudents(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      <h1>Student Management System</h1>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Course</th>
          </tr>
        </thead>

        <tbody>
          {students.map((student) => (
            <tr key={student.id}>
              <td>{student.id}</td>
              <td>{student.name}</td>
              <td>{student.email}</td>
              <td>{student.course}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;

'''Inside the frontend folder, create: 
Dockerfile '''

FROM node:20

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

'''Inside databse create init.sql '''

CREATE TABLE IF NOT EXISTS students (
id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL,
email VARCHAR(100) NOT NULL,
course VARCHAR(100) NOT NULL
);

INSERT INTO students (name, email, course)
VALUES
('aayushii', 'aayushii@gmail.com', 'BSc IT'),
('Priya', 'priya@gmail.com', 'BSc IT'),
('Amit', 'amit@gmail.com', 'BSc IT');

 '''create docker-compose.yml on main folder '''

services:

  frontend:
    build: ./frontend
    container_name: student_frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend

  backend:
    build: ./backend
    container_name: student_backend
    ports:
      - "5000:5000"
    environment:
      DB_HOST: database
      DB_NAME: studentdb
      DB_USER: postgres
      DB_PASSWORD: postgres
    depends_on:
      - database

  database:
    image: postgres:16
    container_name: student_database
    restart: always
    environment:
      POSTGRES_DB: studentdb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  postgres_data:

'''terminal inside three-tier-docker:
docker compose build
docker compose up -d
docker ps
docker compose ps
'''