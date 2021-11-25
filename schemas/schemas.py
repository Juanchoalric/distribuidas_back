from marshmallow import Schema, fields, post_load, ValidationError


class PersonalSchema(Schema):
    legajo = fields.Integer(required=True)
    nombre = fields.String(required=True)
    apellido = fields.String(required=True)
    sector = fields.String(required=True)
    categoria = fields.Integer(required=True)
    fechaIngreso = fields.String()

class CreatePersonalSchema(Schema):
    legajo = fields.Integer(required=True)
    nombre = fields.String(required=True)
    apellido = fields.String(required=True)
    sector = fields.String(required=True)
    categoria = fields.Integer(required=True)
    fechaIngreso = fields.String()
    password = fields.String(required=True)

class VerifiedVecinoSchema():
    documento = fields.Integer(required=True)


class BarrioSchema(Schema):
    idBarrio = fields.Integer(required=True)
    nombre = fields.String(required=True)


class VecinoSchema(Schema):
    documento = fields.Integer(required=True)
    nombre = fields.String(required=True)
    apellido = fields.String(required=True)
    direccion = fields.String()
    codigoBarrio = fields.Integer()

class SitioSchema(Schema):
    idSitio = fields.Integer(required=True)
    latitud = fields.Number()
    longitud = fields.Number()
    calle = fields.String()
    numero = fields.Integer()
    entreCalleA = fields.String()
    entreCalleB = fields.String()
    descripcion = fields.String()
    aCargoDe = fields.String()
    apertura = fields.String()
    cierre = fields.String()
    comentarios = fields.String()

class PublicacionSchema(Schema):
    idPublicidad = fields.Integer(required=True)
    documento = fields.Integer(required=True)
    titulo = fields.String(required=True)
    descripcion = fields.String(required=True)
    type = fields.String(required=True)
    open = fields.String(required=True)
    close = fields.String(required=True)
    imagen = fields.List(fields.String(), required=True)


class RubroSchema(Schema):
    idRubro = fields.Integer(required=True)
    descripcion = fields.String(required=True)

class DesperfectoSchema(Schema):
    idDesperfecto = fields.Integer(required=True)
    descripcion = fields.String(required=True)
    idRubro = fields.Integer(required=True)

class ReclamoSchema(Schema):
    idReclamo = fields.Integer(required=True)
    documento = fields.Integer(required=True)
    idSitio = fields.Integer(required=True)
    idDesperfecto = fields.Integer(required=True)
    descripcion = fields.String(required=True)
    estado = fields.String(required=True)
    IdReclamoUnificado = fields.Integer()
    imagen = fields.List(fields.String(), required=True)

class ReclamoImagenSchema(Schema):
    idReclamo = fields.Integer(required=True)
    imagen = fields.List(fields.String())

class DenunciaSchema(Schema):
    idDenuncias = fields.Integer(required=True)
    documento = fields.Integer(required=True)
    idSitio = fields.Integer(required=True)
    descripcion = fields.String(required=True)
    estado = fields.String(required=True)
    aceptaResponsabilidad = fields.Integer(required=True)
    imagen = fields.List(fields.String(), required=True)

class MovimientosReclamoSchema(Schema):
    idMovimiento = fields.Integer(required=True)
    idReclamo = fields.Integer(required=True)
    responsable = fields.String(required=True)
    causa = fields.String(required=True)
    fecha = fields.DateTime(required=True)

class MovimientosDenunciaSchema(Schema):
    idMovimiento = fields.Integer(required=True)
    idDenuncia = fields.Integer(required=True)
    responsable = fields.String(required=True)
    causa = fields.String(required=True)
    fecha = fields.DateTime(required=True)

class PersonalLogin(Schema):
    legajo = fields.Integer(required=True)
    password = fields.String(required=True)

class VecinoStoragePass(Schema):
    documento = fields.Integer(required=True)
    password = fields.String(required=True)