from flask import Flask, request, jsonify
import sqlite3 as sql
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
import os
from datetime import datetime

DB_PATH = "distribuidas.db"

app = Flask(__name__)

try:
    home = os.path.abspath(os.getcwd())+'\\database\\distribuidas.db'
except:
    home = 'home/juanchoalric/Desktop/distribuidas/database/distribuidas.db'

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///'+home

db = SQLAlchemy(app)

def addValues():
    conn = sql.connect("C:\\Users\\enenadovit\\Desktop\\distribuidas\\distribuidas_back\\database\\distribuidas.db")
    cursor = conn.cursor()
    data = [(1, "belgrano"), (2, "chacarita")]
    cursor.executemany("""INSERT INTO barrios VALUES (?,?)""", data)
    print(cursor.execute("""SELECT * FROM barrios"""))
    conn.close()

class Personal(db.Model):
    __tablename__ = "personal"
    legajo = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String, nullable=False)
    apellido  = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    sector = db.Column(db.String, nullable=False)
    categoria = db.Column(db.Integer, nullable=False)
    fechaIngreso = db.Column(db.DateTime, nullable=False)

class Barrio(db.Model):
    __tablename__ = "barrios"
    idBarrio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)

class Vecino(db.Model):
    __tablename__ = "vecinos"
    documento = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    apellido = db.Column(db.String, nullable=False)
    direccion = db.Column(db.String, nullable=True)
    codigoBarrio = db.Column(db.Integer, db.ForeignKey("Barrio.idBarrio") , nullable=True)
    vecinos_barrios = db.Column(db.Integer)


@app.route("/vecinos", methods=["POST"])
def create_vecino():
    data = request.get_json()
    print(data)
    new_vecino = Vecino(
        documento=data["documento"],
        nombre=data["nombre"],
        apellido=data["apellido"],
        direccion=data["direccion"],
        codigoBarrio=data["codigoBarrio"]
        )
    return ""

@app.route("/vecinos/<vecino_id>", methods=["GET"])
def get_user():
    return ""

@app.route("/vecinos/<vecino_id>", methods=["PUT"])
def update_vecino():
    return ""

@app.route("/personal", methods=["POST"])
def create_personal():
    data = request.get_json()
    print(data)
    new_personal=Personal(
        legajo=data["legajo"],
        nombre=data["nombre"],
        apellido=data["apellido"],
        password=generate_password_hash(data["password"], method="sha256"),
        sector=data["sector"],
        categoria=data["categoria"],
        fechaIngreso=datetime.strptime(data["fechaIngreso"], '%d/%m/%Y')
    )

    db.session.add(new_personal)
    db.session.commit()

    return jsonify({"message": "New Personal Created"})


if (__name__ == "__main__"):
    app.run(port=8082)