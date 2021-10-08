from flask import Flask
import sqlite3 as sql
from flask_sqlalchemy import SQLAlchemy

DB_PATH = "distribuidas.db"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlalchemy:///home/juanchoalric/Desktop/distribuidas/Distribuidas.sql"

db = SQLAlchemy(app)

class Personal(db.Model):
    __tablename__ = "Personal"
    legajo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    apellido  = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    sector = db.Column(db.String, nullable=False)
    category = db.Column(db.Integer, nullable=False)
    fechaIngreso = db.Column(db.DateTime, nullable=False)

class Barrios(db.Model):
    __tablename__ = "Barrios"
    idBarrio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)

class Vecinos(db.Model):
    __tablename__ = "Vecinos"
    documento = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    apellido = db.Column(db.String, nullable=False)
    direccion = db.Column(db.String, nullable=True)
    codigoBarrio = db.Column(db.Integer, nullable=True)
    vecinos_barrios = db.Column(db.Integer, db.ForeignKey("Barrios.idBarrio"))

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    create_db()
    app.run(port=8082)