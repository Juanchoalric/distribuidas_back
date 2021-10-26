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