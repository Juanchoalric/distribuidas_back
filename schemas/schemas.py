from marshmallow import Schema, fields, post_load, ValidationError


class PersonalSchema(Schema):
    legajo = fields.Integer()
    nombre = fields.String()
    apellido = fields.String()
    sector = fields.String()
    categoria = fields.Integer()
    fecha = fields.Date()

class VerifiedVecinoSchema():
    documento = fields.Integer()


class BarrioSchema(Schema):
    idBarrio = fields.Integer()
    nombre = fields.String()


class VecinoSchema(Schema):
    documento = fields.Integer()
    nombre = fields.String()
    apellido = fields.String()
    direccion = fields.String()
    codigoBarrio = fields.Integer()

class SitioSchema(Schema):
    idSitio = fields.Integer()
    latitud = fields.Number()
    longitud = fields.Number()
    calle = fields.String()
    numero = fields.Integer()
    entreCalleA = fields.String()
    entreCalleB = fields.String()
    descripcion = fields.String()
    aCargoDe = fields.String()
    apertura = fields.Time()
    cierre = fields.Time()
    comentarios = fields.String()

class PublicacionSchema(Schema):
    idPublicidad = fields.Integer()
    documento = fields.Integer()
    titulo = fields.String()
    descripcion = fields.String()
    type = fields.String()
    open = fields.String()
    close = fields.String()


class RubroSchema(Schema):
    idRubro = fields.Integer()
    descripcion = fields.String()

class DesperfectoSchema(Schema):
    idDesperfecto = fields.Integer()
    descripcion = fields.String()
    idRubro = fields.String()

class ReclamoSchema(Schema):
    idReclamo = fields.Integer()
    documento = fields.Integer()
    idSitio = fields.Integer()
    idDesperfecto = fields.Integer()
    descripcion = fields.String()
    estado = fields.String()
    idReclamoUnique = fields.Integer()

class ReclamoImagenSchema(Schema):
    idReclamo = fields.Integer()
    documento = fields.Integer()
    imagen = fields.List(fields.String())

class DenunciaSchema(Schema):
    idDenuncia = fields.Integer()
    documento = fields.Integer()
    idSitio = fields.Integer()
    descripcion = fields.String()
    estado = fields.String()
    aceptaResponsabilidad = fields.Integer()

class MovimientosReclamoSchema(Schema):
    idMovimiento = fields.Integer()
    idReclamo = fields.Integer()
    responsable = fields.String()
    causa = fields.String()
    fecha = fields.DateTime()

class MovimientosDenunciaSchema(Schema):
    idMovimiento = fields.Integer()
    idDenuncia = fields.Integer()
    responsable = fields.String()
    causa = fields.String()
    fecha = fields.DateTime()

class PersonalLogin(Schema):
    legajo = fields.Integer()
    password = fields.String()