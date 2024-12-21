from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import environ
import logging
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get('SECRET_KEY', 'default-secret-key')
logging.basicConfig(level=logging.INFO)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        task_name = request.form.get('task_name')
        if task_name:
            new_task = Task(name=task_name)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"Error adding task: {e}")
        db.session.rollback()
        return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host=environ.get('HOST'), debug=bool(int(environ.get('FLASK_DEBUG', 0))))
