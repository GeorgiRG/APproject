from marshmallow import fields, Schema
from schemas.reservation import ReservationSchema


class UserInfoSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    username = fields.String(dump_only=True)
    email = fields.Email(dump_only=True)
    reservations = fields.List(fields.Nested(ReservationSchema, exclude=('user_id', )))
