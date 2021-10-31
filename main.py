import json

from flask import Flask, request, jsonify
import sqlite3 as sql
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import DeclarativeMeta
from pathlib import Path
import os
from marshmallow import ValidationError
from datetime import datetime

from schemas.schemas import PublicacionSchema, PersonalSchema, BarrioSchema, VecinoSchema, SitioSchema, ReclamoSchema, DenunciaSchema, MovimientosReclamoSchema, MovimientosDenunciaSchema, RubroSchema, DesperfectoSchema

DB_PATH = "distribuidas.db"

app = Flask(__name__)

try:
    home = 'sqlite:////' + 'home/juanchoalric/Desktop/distribuidas/database/distribuidas.db'
except:
    home = 'sqlite:///' + os.path.abspath(os.getcwd())+'\\database\\distribuidas.db'

app.config["SQLALCHEMY_DATABASE_URI"] = home
app.config["MONG_DBNAME"] = "distribuidas"
app.config["MONGO_URI"] = "mongodb+srv://dbuser:Mvkvemu7tfb691sS@cluster0.hobus.mongodb.net/distribuidas?retryWrites=true&w=majority"

db = SQLAlchemy(app)
db_mongo = PyMongo(app).db

personal_schema = PersonalSchema(many=True)
personal_single_schema = PersonalSchema()
barrio_schema = BarrioSchema(many=True)
barrio_single_schema = BarrioSchema()
vecino_schema = VecinoSchema(many=True)
vecino_single_schema = VecinoSchema()
sitio_schema = SitioSchema(many=True)
sitio_single_schema = SitioSchema()
rubro_schema = RubroSchema(many=True)
rubro_single_schema = RubroSchema()
reclamo_schema = ReclamoSchema(many=True)
reclamo_single_schema = ReclamoSchema()
denuncia_schema = DenunciaSchema(many=True)
denuncia_single_schema = DenunciaSchema()
desperfecto_schema = DesperfectoSchema(many=True)
desperfecto_single_schema = DesperfectoSchema()
movimientos_reclamo_schema = MovimientosReclamoSchema(many=True)
movimientos_reclamo_single_schema = MovimientosReclamoSchema()
movimientos_denuncia_schema = MovimientosDenunciaSchema(many=True)
movimientos_denuncia_single_schema = MovimientosDenunciaSchema()
publicaciones_schema = PublicacionSchema(many=True)
publicacion_schema = PublicacionSchema()

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
    codigoBarrio = db.Column(db.Integer, db.ForeignKey("barrios.idBarrio"))


class Sitio(db.Model):
    __tablename__ = "sitios"
    idSitio = db.Column(db.Integer, primary_key=True)
    latitud = db.Column(db.Numeric(9, 5), nullable=False)
    longitud = db.Column(db.Numeric(9, 5), nullable=False)
    calle = db.Column(db.String, nullable=True)
    numero = db.Column(db.Integer, nullable=True)
    entreCalleA = db.Column(db.String, nullable=True)
    entreCalleB = db.Column(db.String, nullable=True)
    descripcion = db.Column(db.String, nullable=True)
    aCargoDe = db.Column(db.String, nullable=True)
    apertura = db.Column(db.Time, nullable=True)
    cierre = db.Column(db.Time, nullable=True)
    comentatios = db.Column(db.Text, nullable=True)


class Rubro(db.Model):
    __tablename__ = "rubros"
    idRubro = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String, nullable=False)


class Desperfecto(db.Model):
    __tablename__ = "desperfectos"
    idDesperfecto = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String, nullable=False)
    idRubro = db.Column(db.Integer, db.ForeignKey("rubros.idRubro"))


class Reclamo(db.Model):
    __tablename__ = "reclamos"
    idReclamo = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String, db.ForeignKey("vecinos.documento"))
    descripcion = db.Column(db.String, nullable=True)
    estado = db.Column(db.String)
    idSitio = db.Column(db.Integer, db.ForeignKey("sitios.idSitio"))
    idDesperfecto = db.Column(db.Integer, db.ForeignKey("desperfectos.idDesperfecto"))
    IdReclamoUnificado = db.Column(db.Integer, db.ForeignKey("reclamos.idReclamo"))

class Denuncia(db.Model):
    idDenuncia = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String, db.ForeignKey("vecinos.documento"), nullable=False)
    idSitio = db.Column(db.Integer, db.ForeignKey("sitios.idSitio"), nullable=True)
    descripcion = db.Column(db.String, nullable=True)
    estado = db.Column(db.String)
    aceptaResponsabilidad = db.Column(db.Integer, nullable=False)
    

class MovimientosReclamo(db.Model):
    __tablename__ = "movimientosReclamo"
    idMovimiento = db.Column(db.Integer, primary_key=True)
    responsable = db.Column(db.String, nullable=False)
    causa = db.Column(db.String, nullable=False)
    fecha = db.Column(db.DateTime)
    idReclamo = db.Column(db.Integer, db.ForeignKey("reclamos.idReclamo"))

class MovimientosDenuncia(db.Model):
    __tablename__ = "movimientosDenuncia"
    idMovimiento = db.Column(db.Integer, primary_key=True)
    responsable = db.Column(db.String, nullable=False)
    causa = db.Column(db.String, nullable=False)
    fecha = db.Column(db.DateTime)
    idDenuncia = db.Column(db.Integer, db.ForeignKey("denuncias.idDenuncia"))

@app.route("/publicidad", methods=["GET", "POST"])
def create_publicidad():
    if request.method == "POST":
        data = request.get_json()
        try:
            data = publicacion_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages)
        db_mongo.publicidad.insert_one({
            "_id": data["idPublicidad"],
            "documento": data["documento"],
            "titulo": data["titulo"],
            "descripcion": data["descripcion"],
            "type": data["type"],
            "open": data["open"],
            "close": data["close"]
        })
        return jsonify({"Message": "Publicidad Created"})
    if request.method == "GET":
        publicidad = db_mongo.publicidad.find({})
        return jsonify(publicaciones_schema.dump(publicidad))


@app.route("/sitio", methods=["POST", "GET"])
def create_sitio():
    if request.method == "POST":
        data = request.get_json()
        try:
            data = sitio_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages)

        new_sitio = Sitio(
            idSitio = data.get("idSitio"),
            latitud = data.get("latitud"),
            longitud = data.get("longitud"),
            calle = data.get("calle"),
            numero = data.get("numero"),
            entreCalleA = data.get("entreCalleA"),
            entreCalleB = data.get("entreCalleB"),
            descripcion = data.get("descripcion"),
            aCargoDe = data.get("aCargoDe"),
            apertura = data.get("apertura"),
            cierre = data.get("cierre"),
            comentarios = data.get("comentarios")
        )

        db.session.add(new_sitio)
        db.session.commit()
    if request.method == "GET":
        sitios = db.session.query(Sitio).all()
        return jsonify(sitio_schema.dump(sitios))

@app.route("/rubros", methods=["GET", "POST"])
def create_rubros():
    if request.method == "POST":
        data = request.get_json()
        try:
            data = rubro_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages)

        new_rubro = Rubro(
            idRubro = data["idRubro"],
            description = data["description"],
        )

        db.session.add(new_rubro)
        db.session.commit()
    if request.method == "GET":
        rubros = db.session.query(Rubro).all()
        return jsonify(rubro_schema.dump(rubros))
    
@app.route("/reclamo", methods=["GET", "POST"])
def create_reclamo():
    if request.method == "POST":
        data = request.get_json()
        try:
            data = reclamo_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages)

        new_reclamo = Reclamo(
            idReclamo=data["idReclamo"],
            documento = data["documento"],
            idSitio = data["idSitio"],
            idDesperfecto = data["idDesperfecto"],
            description = data["description"],
            estado = data["estado"],
            idReclamoUnique=data["idReclamoUnique"],
        )
    
        db.session.add(new_reclamo)
        db.session.commit()

    if request.method == "GET":
        reclamos = db.session.query(Reclamo).all()
        return jsonify(reclamo_schema.dump(reclamos))

@app.route('/despecfecto', methods=['GET', 'POST'])
def create_desperfecto():
    
    if request.method == "POST":
        data = request.get_json()
        try:
            data = desperfecto_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages)

        new_desperfecto = Desperfecto(
            idDesperfecto = data['idDesperfecto'],
            description = data['description'],
            idRubro = data['idRubro'],
        )

        db.session.add(new_desperfecto)
        db.session.commit()
    
    if request.method == 'GET':
        desperfectos = db.session.query(Desperfecto).all()
        return jsonify(desperfecto_schema.dump(desperfectos))


@app.route('/denuncia', methods=['POST', "GET"])
def create_denuncia():
    if request.method == 'POST':
        data = request.get_json()
        try:
            data = denuncia_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages)

        new_denuncia = Denuncia(
            idDenuncia = data["idDenuncia"],
            documento = data["documento"],
            idSitio = data["idSitio"],
            description = data["description"],
            estado = data["estado"],
            aceptaResponsabilidad = data["aceptaResponsabilidad"],
        )
        db.session.add(new_denuncia)
        db.session.commit()
    if request.method == "GET":
        denuncias = db.session.query(Denuncia).all()
        return jsonify(denuncia_schema.dump(denuncias))

@app.route('/movimientosReclamo', methods=["GET", "POST"])
def create_movimientos_reclamo():
    if request.method == "POST":
        data = request.get_json()
        try:
            data = movimientos_reclamo_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages)

        new_movimientos_reclamo = MovimientosReclamo(
            idMovimiento = data["idMovimiento"],
            idReclamo = data["idReclamo"],
            responsable = data["responsable"],
            causa = data["causa"],
            fecha = datetime.strptime(data["fecha"], '%Y-%m-%d %H:%M:%S.%f')
        )

        db.session.add(new_movimientos_reclamo)
        db.session.commit()
    if request.method == "GET":
        movimientos_reclamo = db.session.query(MovimientosReclamo).all()
        return jsonify(movimientos_reclamo_schema.dump(movimientos_reclamo))

@app.route('/movimientosDenuncia', methods=["GET", "POST"])
def create_movimientos_denuncia():
    if request.method == "POST":
        data = request.get_json()
        try:
            data = movimientos_denuncia_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages)

        new_movimientos_denuncia = MovimientosDenuncia(
            idMovimiento=data["idMovimiento"],
            idDenuncia=data["idDenuncia"],
            responsable = data["responsable"],
            causa = data["causa"],
            fecha = datetime.strptime(data["fecha"], '%Y-%m-%d %H:%M:%S.%f'),
        )
        db.session.add(new_movimientos_denuncia)
        db.session.commit()
    if request.method == "GET":
        movimientos_denuncia = db.session.query(MovimientosDenuncia).all()
        return jsonify(movimientos_denuncia_schema.dump(movimientos_denuncia))


@app.route("/barrio", methods=["POST", "GET"])
def create_barrio():
    if request.method == "POST":
        data = request.get_json()

        try:
            data = movimientos_reclamo_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages)

        new_barrio = Barrio(
            idBarrio=data.get("idBarrio"),
            nombre=data.get("nombre")
        )

        db.session.add(new_barrio)
        db.session.commit()

        return jsonify({"message": "Barrio created"})
    if request.method == "GET":
        barrios = db.session.query(Barrio).all()
        return jsonify(barrio_schema.dump(barrios))


@app.route("/vecinos", methods=["POST", "GET"])
def create_vecino():
    if request.method == "POST":
        data = request.get_json()
        try:
            data = vecino_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages)

        new_vecino = Vecino(
            documento=data["documento"],
            nombre=data["nombre"],
            apellido=data["apellido"],
            direccion=data["direccion"],
            codigoBarrio=data["codigoBarrio"]
            )

        db.session.add(new_vecino)
        db.session.commit()
        return jsonify({"message": "Vecino created"})

    if request.method == "GET":
        vecinos = db.session.query(Vecino).all()
        vecinos = vecino_schema.dump(vecinos)
        return jsonify(vecino_schema.dump(vecinos))


@app.route("/vecinos/<vecino_id>", methods=["GET"])
def get_user():
    return ""


@app.route("/vecinos/<vecino_id>", methods=["PUT"])
def update_vecino():
    return ""


@app.route("/personal", methods=["POST"])
def create_personal():
    data = request.get_json()
    try:
        data = personal_single_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages)

    new_personal=Personal(
        legajo=data["legajo"],
        nombre=data["nombre"],
        apellido=data["apellido"],
        password=generate_password_hash(data["password"], method="sha256"),
        sector=data["sector"],
        categoria=data["categoria"],
        fechaIngreso=datetime.strptime(data["fechaIngreso"], '%d/%m/%Y')
    )

    db.session.add(json.dump(new_personal))
    db.session.commit()

    return jsonify({"message": "New Personal Created"})


@app.route("/personal", methods=["GET"])
def get_personal():
    personal = db.session.query(Personal).all()
    personal = personal_schema.dump(personal)
    return jsonify(personal)


if __name__ == "__main__":
    app.run(port=8082)
