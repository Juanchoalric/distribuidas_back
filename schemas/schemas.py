from marshmallow import Schema, fields


class PersonalSchema(Schema):
    legajo = fields.Integer()
    nombre = fields.String()
    apellido = fields.String()
    sector = fields.String()
    categoria = fields.Integer()
    fecha = fields.Date()
