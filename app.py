import os
from datetime import datetime
from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

#init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init DB
db = SQLAlchemy(app)
#Init Masrshmallow
ma = Marshmallow(app)

#Todo Class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    desc = db.Column(db.String(200))
    cat = db.Column(db.String(20))
    due = db.Column(db.DateTime)
    active = db.Column(db.Boolean)

    def __init__(self, name, desc, cat, due, active):
        self.name = name
        self.desc = desc
        self.cat = cat
        self.due = due
        self.active = active

#Todo Schema
class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'desc', 'cat', 'due', 'active')
#Init Schema
todos_schema = TodoSchema(many = True)
todo_schema = TodoSchema()

#Create Todo
@app.route('/todo', methods=['POST'])
def add_todo():
    name = request.json['name']
    desc = request.json['desc']
    cat = request.json['cat']
    due = request.json['due']
    active = request.json['active']

    fdue = datetime.strptime(due, '%Y-%m-%d')

    new_todo = Todo(name, desc, cat, fdue, active)

    db.session.add(new_todo)
    db.session.commit()

    return todo_schema.jsonify(new_todo)

#Get All Todo's
@app.route('/todo', methods=['GET'])
def get_todos():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result)

#Get Single Todo
@app.route('/todo/<id>', methods=['GET'])
def get_todo(id):
    todo = Todo.query.get(id)
    return todo_schema.jsonify(todo)

#Update Todo
@app.route('/todo/<id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get(id)

    name = request.json['name']
    desc = request.json['desc']
    cat = request.json['cat']
    due = request.json['due']
    active = request.json['active']

    fdue = datetime.strptime(due, '%Y-%m-%d')

    todo.name = name
    todo.desc = desc
    todo.cat = cat
    todo.due = fdue
    todo.active = active

    db.session.commit()

    return todo_schema.jsonify(todo)

#Delete Todo
@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    
    return todo_schema.jsonify(todo)


#Run Server
if __name__ == '__main__':
    app.run(debug=True)
