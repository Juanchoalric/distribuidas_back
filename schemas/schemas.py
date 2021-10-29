from marshmallow import Schema, fields


class PersonalSchema(Schema):
    legajo = fields.Integer()
    nombre = fields.String()
    apellido = fields.String()
    sector = fields.String()
    categoria = fields.Integer()
    fecha = fields.Date()


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
    latitud = fields.decimal()
    longitud = fields.decimal()
    calle = fields.String()
    numero = fields.Integer()
    entreCalleA = fields.String()
    entreCalleB = fields.String()
    descripcion = fields.String()
    aCargoDe = fields.String()
    apertura = fields.Time()
    cierre = fields.Time()
    comentarios = fields.String()

class RubroSchema(Schema):
    idRubro = fields.Integer()
    descripcion = fields.String()

class DesperfectoSchema(Schema):
    idDesperfecto = fields.Integer()
    descripcion = fields.String()
    idRubro = fields.String()

class ReclamoSchema(Schema):
    idReclamo = fields.Integer()
    documento = fields.String()
    idSitio = fields.Integer()
    idDesperfecto = fields.Integer()
    descripcion = fields.String()
    estado = fields.String()
    idReclamoUnique = fields.Integer()

class DenunciaSchema(Schema):
    idDenuncia = fields.Integer()
    documento = fields.String()
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