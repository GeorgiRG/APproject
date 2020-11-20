from marshmallow import fields, Schema

from schemas.user import UserSchema


class ReservationSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    start_time = fields.DateTime(format="%d/%m/%Y %H:%M", required=True)
    end_time = fields.DateTime(format="%d/%m/%Y %H:%M", dump_only=True)
    duration = fields.String()
    created_at = fields.DateTime(dump_only=True)
    user_id = fields.Nested(UserSchema, dump_only=True, only=("id", ))
    reserved_by = fields.String()
    workspace = fields.String()
