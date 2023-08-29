from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo-db.sqlite'

db = SQLAlchemy(app)

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100))
    done = db.Column(db.Boolean, default=False)

    def __init__(self, task):
        self.task = task

@app.route('/')
def index():
    todo_list = TodoItem.query.all()
    return render_template('index.html', todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    todo_item = TodoItem(task=task)
    db.session.add(todo_item)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo_item = TodoItem.query.filter_by(id=todo_id).first()
    todo_item.done = not todo_item.done
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo_item = TodoItem.query.filter_by(id=todo_id).first()
    db.session.delete(todo_item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)