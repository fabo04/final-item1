from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Creo la variable "db" que me permitira conectarme con la base de datos asociada a la App
db = SQLAlchemy()

# Modelos de Datos
class Task(db.Model):
    id = db.Column(db.String(250), primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text())
    user_id = db.Column(db.String(250), db.ForeignKey('user.id'), nullable=False)

class History(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date_in = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(50))
    user_id = db.Column(db.String(250), db.ForeignKey('user.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.String(250), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80))
    task = db.relationship('Task', backref='user', lazy=True)
    history = db.relationship('History', backref='user', lazy=True)

    def __str__ (self):
        return f'Id: {self.id}, Nombre de Usuario: {self.username}, E-mail: {self.email}'
