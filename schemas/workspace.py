from marshmallow import Schema, fields, validate


class WorkspaceSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    workspace_number = fields.String(required=True, validate=[validate.Length(max=4)])
    turkuamk_only = fields.Boolean(required=True)
    available_space = fields.Integer()