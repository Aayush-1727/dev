'''postgre sql shud be installed and docker too

cmd
python --version
node --version
npm --version

For PostgreSQL:
"C:\Program Files\PostgreSQL\18\bin\psql.exe" --version
netstat -ano | findstr :5433
 
new cmd
cd %USERPROFILE%\Desktop
mkdir three-tier-student-app
cd three-tier-student-app
mkdir backend
mkdir frontend

search  pgAdmin and open
Go to:
Servers → PostgreSQL 18 → Databases
Right-click Databases → Create → Database
Database: studentdb2
save.
'''
'''In pgAdmin, select:
studentdb2 right click for "Query Tool" '''
CREATE TABLE students (
id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL,
email VARCHAR(100) NOT NULL,
course VARCHAR(100) NOT NULL
);

INSERT INTO students (name, email, course)
VALUES
('aayushi', 'aayushi@gmail.com', 'IT')
('saloni', 'saloni@gmail.com', 'IT')
('tanu', 'tanu@gmail.com', 'DS')
#run it.

'''cmd
cd %USERPROFILE%\Desktop\three-tier-student-app
cd backend
python -m venv venv
venv\Scripts\activate
python -m pip install flask flask-cors "psycopg[binary]"
python -c "import flask, psycopg; print ('Flask and PostgreSQL connector OK')" 
code .

Inside the backend folder, create a file named:
app.py
'''
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg

app = Flask(__name__)
CORS(app)

# PostgreSQL connection
DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "studentdb2",
    "user": "postgres",
    "password": "YOUR_POSTGRES_PASSWORD"
}

def get_connection():
    return psycopg.connect(**DB_CONFIG)

@app.route("/")
def home():
    return jsonify({
        "message": "Student Management API is running"
    })

@app.route("/students", methods=["GET"])
def get_students():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, email, course FROM students ORDER BY id"
    )

    students = cur.fetchall()

    cur.close()
    conn.close()

    result = []

    for student in students:
        result.append({
            "id": student[0],
            "name": student[1],
            "email": student[2],
            "course": student[3]
        })

    return jsonify(result)

@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    course = data.get("course")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO students (name, email, course)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (name, email, course)
    )

    student_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "message": "Student added successfully",
        "id": student_id
    }), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)

'''Replace YOUR_POSTGRES_PASSWORD
Go back to Command Prompt.
Make sure you are still inside:
three-tier-student-app\backend
and that (venv) is visible.
python app.py'''

"Till here backend + db"
'''
new cmd open, keep old one running in background
cd %USERPROFILE%\Desktop\three-tier-student-app
npm create vite@latest frontend -- --template react
enter "y"
cd frontend
npm install
npm install axios

open vs in frontend > src > App.jsx,replace whole code: '''

import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/students")
      .then((response) => {
        setStudents(response.data);
      })
      .catch((error) => {
        console.error("Error fetching students:", error);
      });
  }, []);

  return (
    <div className="container">
      <h1>Student Management System</h1>

      <table>
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

'''same for App.css whole code to be replaced:'''

body {
  font-family: Arial, sans-serif;
  background: #f2f2f2;
  margin: 0;
  padding: 40px;
}

.container {
  max-width: 900px;
  margin: auto;
  background: white;
  padding: 30px;
  border-radius: 10px;
}

h1 {
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 25px;
}

th,
td {
  border: 1px solid #ccc;
  padding: 12px;
  text-align: left;
}

th {
  background: #eeeeee;
}

'''In frontend vala cmd 
npm run dev

'''