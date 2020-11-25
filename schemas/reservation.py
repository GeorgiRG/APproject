from marshmallow import fields, Schema, validate

from schemas.user import UserSchema


class ReservationSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    start_time = fields.DateTime(format="%d/%m/%Y %H:%M", required=True)
    end_time = fields.DateTime(format="%d/%m/%Y %H:%M", dump_only=True)
    duration = fields.String(required=True)
    attendees = fields.Integer(validate=[validate.Range(min=1, max=30)], required=True)
    created_at = fields.DateTime(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    reserved_by = fields.String()
    workspace = fields.String(required=True,validate=[validate.Length(max=4)])
