'''
cmd
python --version

desktop
Flask_Project
open cmd frm this folder
python -m venv venv
venv\Scripts\activate
pip install flask

open vs app.py
'''
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)

'''
open cmd
python app.py

code2
'''
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to my first Flask API",
        "status": "success"
    })

if __name__ == '__main__':
    app.run(debug=True)

'''python app.py'''

code3

from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data storage
todos = [
    {
        "id": 1,
        "title": "Learn Flask",
        "completed": False
    }
]

# CREATE a new task
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()

    new_todo = {
        "id": len(todos) + 1,
        "title": data['title'],
        "completed": False
    }

    todos.append(new_todo)
    return jsonify(new_todo), 201


# READ all tasks
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)


# READ a single task
@app.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todo = next((t for t in todos if t['id'] == id), None)

    if todo is None:
        return jsonify({"message": "Task not found"}), 404

    return jsonify(todo)


# UPDATE a task
@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = next((t for t in todos if t['id'] == id), None)

    if todo is None:
        return jsonify({"message": "Task not found"}), 404

    data = request.get_json()

    todo['title'] = data.get('title', todo['title'])
    todo['completed'] = data.get('completed', todo['completed'])

    return jsonify(todo)


# DELETE a task
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    global todos

    todo = next((t for t in todos if t['id'] == id), None)

    if todo is None:
        return jsonify({"message": "Task not found"}), 404

    todos = [t for t in todos if t['id'] != id]

    return jsonify({"message": "Task deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)

'''python app.py'''
