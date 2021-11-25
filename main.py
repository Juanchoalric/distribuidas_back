import json

from flask import Flask, request, jsonify
import sqlite3 as sql
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import DeclarativeMeta
from pathlib import Path
import os
import random
from marshmallow import ValidationError
from datetime import datetime
from sys import platform
import base64

from schemas.schemas import CreatePersonalSchema, VecinoStoragePass, VerifiedVecinoSchema, PublicacionSchema, ReclamoImagenSchema, PersonalLogin, PersonalSchema, BarrioSchema, VecinoSchema, SitioSchema, ReclamoSchema, DenunciaSchema, MovimientosReclamoSchema, MovimientosDenunciaSchema, RubroSchema, DesperfectoSchema

DB_PATH = "distribuidas.db"

app = Flask(__name__)

if platform == "win32":
    home = 'sqlite:///' + os.path.abspath(os.getcwd())+'\\database\\distribuidas.db'
else:
    home = 'sqlite:////' + 'home/juanchoalric/Desktop/distribuidas/database/distribuidas.db'

app.config["SQLALCHEMY_DATABASE_URI"] = home
app.config["MONG_DBNAME"] = "distribuidas"
app.config["MONGO_URI"] = "mongodb+srv://dbuser:Mvkvemu7tfb691sS@cluster0.hobus.mongodb.net/distribuidas?retryWrites=true&w=majority"

db = SQLAlchemy(app)
db_mongo = PyMongo(app).db

personal_schema = PersonalSchema(many=True)
personal_single_schema = PersonalSchema()
create_personal_schema = CreatePersonalSchema()
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
reclamo_images_schema = ReclamoImagenSchema()
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
personal_login_schema = PersonalLogin()
verify_vecino_schema = VerifiedVecinoSchema()
vecino_register_password = VecinoStoragePass()

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
    comentarios = db.Column(db.Text, nullable=True)


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
    __tablename__ = "denuncias"
    idDenuncias = db.Column(db.Integer, primary_key=True)
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
        pub_ver = db_mongo.publicidad_verificacion.find_one({"_id": data.get("titulo")})
        if not pub_ver:
            return jsonify({"message": "Todavia no esta verificado"})
        try:
            data["idPublicidad"] = random.getrandbits(10)
            data = publicacion_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages, 404), 404
        db_mongo.publicidad.insert_one({
            "_id": data["idPublicidad"],
            "documento": data["documento"],
            "titulo": data["titulo"],
            "descripcion": data["descripcion"],
            "type": data["type"],
            "open": data["open"],
            "close": data["close"],
            "imagen": data["imagen"]
        })
        return jsonify({"message": "Publicidad Created"})
    if request.method == "GET":
        publicidad = db_mongo.publicidad.find({})
        return jsonify(publicaciones_schema.dump(publicidad))


@app.route("/sitio", methods=["POST", "GET"])
def create_sitio():
    if request.method == "POST":
        data = request.get_json()
        try:
            data["idSitio"] = random.getrandbits(20)
            data = sitio_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages, 404), 404

        apertura = datetime.strptime(data["apertura"] ,"%H:%M:%S")
        cierre = datetime.strptime(data["cierre"] ,"%H:%M:%S")
        print(type(apertura))
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
            apertura = apertura.time(),
            cierre = cierre.time(),
            comentarios = data.get("comentarios")
        )

        db.session.add(new_sitio)
        db.session.commit()
    if request.method == "GET":
        sitios = db.session.query(Sitio).all()
        return jsonify(sitio_schema.dump(sitios))

@app.route("/rubro", methods=["GET", "POST"])
def create_rubros():
    if request.method == "POST":
        data = request.get_json()
        try:
            data["idRubro"] = random.getrandbits(10)
            data = rubro_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages, 404), 404

        new_rubro = Rubro(
            idRubro = data["idRubro"],
            descripcion = data["descripcion"],
        )

        db.session.add(new_rubro)
        db.session.commit()
        return jsonify({"message": "Rubro created"})
    if request.method == "GET":
        rubros = db.session.query(Rubro).all()
        return jsonify(rubro_schema.dump(rubros))
    
@app.route("/reclamo", methods=["GET", "POST", "DELETE"])
def create_reclamo():
    if request.method == "POST":
        data = request.get_json()
        try:
            data["idReclamo"] = random.getrandbits(10)
            data = reclamo_single_schema.load(data)
            db_mongo.reclamos_imagen.insert_one({"_id": data["idReclamo"], "imagen": data["imagen"]})
        except ValidationError as e:
            return jsonify(e.messages, 404), 404

        new_reclamo = Reclamo(
            idReclamo=data["idReclamo"],
            documento = data["documento"],
            idSitio = data["idSitio"],
            idDesperfecto = data["idDesperfecto"],
            descripcion = data["descripcion"],
            estado = data["estado"],
            IdReclamoUnificado=data.get("IdReclamoUnificado", None),
        )

        db.session.add(new_reclamo)
        db.session.commit()
        return jsonify({"message": "Reclamo Created"})
    if request.method == "GET":
        reclamos = db.session.query(Reclamo).all()
        reclamos = reclamo_schema.dump(reclamos)
        for reclamo in reclamos:
            reclamo_images = db_mongo.reclamos_imagen.find_one({"_id": reclamo["idReclamo"]})
            reclamo["imagen"] = reclamo_images.get("imagen", "")
        return jsonify(reclamos)
    if request.method == "DELETE":
        try:
            db.session.query(Reclamo).delete()
            #db.session.delete(reclamo)
            db.session.commit()
            return jsonify({"message": "Borrado de los reclamos"}), 200
        except Exception as e:
            return jsonify({"message": "no funciono"}), 404


@app.route("/reclamo/<idReclamo>", methods=["GET"])
def get_reclamo(idReclamo):
    if request.method == "GET":
        reclamo = db.session.query(Reclamo).filter_by(idReclamo=idReclamo).first()
        reclamo_imagen = db_mongo.reclamos_imagen.find_one({"_id":idReclamo})
        if not reclamo:
            return jsonify({"message": "Reclamo mal ingresado"}, 404)
        reclamo = reclamo_single_schema.dump(reclamo)
        reclamo["imagen"] = reclamo_imagen["imagen"]
        return jsonify(reclamo)

@app.route('/reclamo/estado', methods=['PUT'])
def update_reclamo_state():
    estado = request.args.get('estado')
    idReclamo = int(request.args.get('idReclamo'))

    reclamo = db.session.query(Reclamo).filter_by(idReclamo=idReclamo).first()

    if not reclamo:
        return jsonify({"message": "El reclamo no existe"})

    reclamo.estado = estado
    db.session.commit()

    return jsonify({"message": "El estado del reclamo se modifico correctamente"}, 200), 200


@app.route('/desperfecto', methods=['GET', 'POST'])
def create_desperfecto():
    
    if request.method == "POST":
        data = request.get_json()
        try:
            data["idDesperfecto"] = random.getrandbits(10)
            data = desperfecto_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages, 404), 404

        new_desperfecto = Desperfecto(
            idDesperfecto = data['idDesperfecto'],
            descripcion = data['descripcion'],
            idRubro = data['idRubro'],
        )

        db.session.add(new_desperfecto)
        db.session.commit()
        return jsonify({"message": "Desperfecto Created"})
    if request.method == 'GET':
        desperfectos = db.session.query(Desperfecto).all()
        return jsonify(desperfecto_schema.dump(desperfectos))


@app.route('/denuncia', methods=['POST', "GET"])
def create_denuncia():
    if request.method == 'POST':
        data = request.get_json()
        try:
            data["idDenuncias"] = random.getrandbits(10)
            data = denuncia_single_schema.load(data)
            db_mongo.denuncias_imagen.insert_one({"_id": data["idDenuncias"], "imagen": data["imagen"]})
        except ValidationError as e:
            return jsonify(e.messages, 404), 404

        new_denuncia = Denuncia(
            idDenuncias = data["idDenuncias"],
            documento = data["documento"],
            idSitio = data["idSitio"],
            descripcion = data["descripcion"],
            estado = data["estado"],
            aceptaResponsabilidad = data["aceptaResponsabilidad"],
        )
        db.session.add(new_denuncia)
        db.session.commit()
        return jsonify({"message": "Denuncia creada"}, 201), 201

    if request.method == "GET":
        denuncias = db.session.query(Denuncia).all()
        print(denuncias)
        denuncias = denuncia_schema.dump(denuncias)
        for denuncia in denuncias:
            denuncia_images = db_mongo.denuncias_imagen.find_one({"_id": denuncia["idDenuncias"]})
            denuncia["imagen"] = denuncia_images["imagen"]
        return jsonify(denuncias)

@app.route("/denuncia/<idDenuncias>", methods=["GET"])
def get_denuncia(idDenuncias):
    if request.method == "GET":
        denuncia = db.session.query(Denuncia).filter_by(idDenuncias=idDenuncias).first()
        denuncia_imagen = db_mongo.denuncias_imagen.find_one({"_id":int(idDenuncias)})
        if not denuncia:
            return jsonify({"message": "Reclamo mal ingresado"}, 404)
        denuncia = denuncia_single_schema.dump(denuncia)
        denuncia["imagen"] = denuncia_imagen["imagen"]
        return jsonify(denuncia)


@app.route('/denuncia/estado', methods=['PUT'])
def update_denuncia_state():
    estado = request.args.get('estado')
    idDenuncias = int(request.args.get('idDenuncias'))

    denuncia = db.session.query(Denuncia).filter_by(idDenuncias=idDenuncias).first()

    if not denuncia:
        return jsonify({"message": "La denuncia no existe"})

    denuncia.estado = estado
    db.session.commit()

    return jsonify({"message": "El estado de la denuncia se modifico correctamente"}, 200), 200


@app.route('/movimientosReclamo', methods=["GET", "POST"])
def create_movimientos_reclamo():
    if request.method == "POST":
        data = request.get_json()
        try:
            data["idMovimiento"] = random.getrandbits(10)
            data = movimientos_reclamo_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages, 404), 404

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
            data["idMovimiento"] = random.getrandbits(10)
            data = movimientos_denuncia_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages, 404), 404

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
            data["idBarrio"] = random.getrandbits(10)
            data = movimientos_reclamo_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages, 404), 404

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


@app.route("/vecinos/create_password", methods=["POST"])
def vecino_create_password():
    data = request.get_json()
    vecino = db_mongo.verified_vecino.find_one({"_id": data.get("documento")})
    if not vecino:
        return jsonify({"message": "No autorizado"}, 400)
    try:
        data = vecino_register_password.load(data)
    except ValidationError as e:
        return jsonify(e.messages, 404), 404

    db_mongo.vecinos.insert_one({
        "_id": data["documento"],
        "password": generate_password_hash(data["password"], method="sha256")
    })
    return jsonify(vecino), 200


@app.route("/vecinos", methods=["POST", "GET"])
def create_vecino():
    if request.method == "POST":
        data = request.get_json()
        try:
            data = vecino_single_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages, 404), 404

        try:
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
        except:
            return jsonify({"response":"Vecino no creado", "code": 404}), 404

    if request.method == "GET":
        vecinos = db.session.query(Vecino).all()
        vecinos = vecino_schema.dump(vecinos)
        return jsonify(vecino_schema.dump(vecinos))


@app.route("/vecinos/verified/<documento>", methods=["GET"])
def is_user_verified(documento):
    vecino = db_mongo.verified_vecino.find_one({"_id": int(documento)})
    if vecino:
        return jsonify({"message": True, "vecino": vecino})
    
    return jsonify({"message": False})


@app.route("/vecino/login", methods=["POST"])
def vecino_login():
    data = request.get_json()
    try:
        data = vecino_register_password.load(data)
    except ValidationError as e:
        return jsonify(e.messages, 404), 404

    vecino = db_mongo.vecinos.find_one({"_id": data["documento"]})

    if not vecino:
        return jsonify({"message": "El documento o password son erroneos"}), 400
    
    if check_password_hash(vecino["password"], data["password"]):
        vecino = db.session.query(Vecino).filter_by(documento=data["documento"]).first()
        return jsonify(vecino_single_schema.dump(vecino))
    return jsonify({"message": "El documento o password son erroneos"}), 400
    
    

@app.route("/vecinos/<vecino_id>", methods=["GET"])
def get_user():
    return ""


@app.route("/vecinos/<documento>", methods=["DELETE"])
def delete_vecino(documento):
    try:
        vecino = db.session.query(Vecino).filter_by(documento=int(documento)).first()
        db.session.delete(vecino)
        db.session.commit()
        return jsonify({"message": "Vecino borrado"})
    except:
        return jsonify({"message": "Vecino no borrado"})

@app.route("/personal", methods=["POST"])
def create_personal():
    data = request.get_json()
    try:
        data = create_personal_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages, 404), 404

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

@app.route("/personal/<legajo>", methods=["GET"])
def get_one_personal(legajo):

    personal = Personal.query.filter_by(legajo=legajo).first()

    if not personal:
        return jsonify({"message": "No Personal Found"})
    
    personal_data = {
        "legajo" : personal.legajo,
        "nombre" : personal.nombre,
        "apellido" : personal.apellido,
        "sector" : personal.sector,
        "categoria" : personal.categoria,
        "fechaIngreso" : personal.fechaIngreso,
    }

    return jsonify(personal_data)

@app.route("/personal", methods=["GET"])
def get_personal():
    personal = db.session.query(Personal).all()
    personal = personal_schema.dump(personal)
    return jsonify(personal)

@app.route("/personal/login", methods=["POST"])
def login_personal():
    data = request.get_json()
    data = personal_login_schema.load(data)
    personal = db.session.query(Personal).filter_by(legajo=data["legajo"]).first()

    if check_password_hash(personal.password, data["password"]):
        return jsonify(personal_single_schema.dump(personal))
    
    return jsonify({"mensaje": "No existe el usuario ingresado", "code": 404}), 404

if __name__ == "__main__":
    app.run(port=8082)
