from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus
from marshmallow import EXCLUDE

from utils import check_admin, check_email
from models.user import User

from schemas.user import UserSchema
from schemas.find_user import UserInfoSchema


user_schema = UserSchema()
user_schema_noadm = UserSchema(exclude=("is_admin", ))
user_schema_outsider = UserSchema(exclude=("is_turkuamk", "is_admin"))


class UserResource(Resource):
    def post(self):
        json_data = request.get_json()
        data = user_schema.load(json_data)
        admin = check_admin(data.get("admin_pass"))
        data = UserSchema(unknown=EXCLUDE).load(json_data)

        if admin and check_email(data.get("email")):
            user = User(is_admin=True, is_turkuamk=True, **data)
            user.save()
            return UserSchema().dump(user), HTTPStatus.CREATED

        elif check_email(data.get('email')):
            user = User(is_turkuamk=True, **data)
            user.save()
            return user_schema_noadm.dump(user), HTTPStatus.CREATED

        else:
            user = User(**data)
            user.save()
            return user_schema_outsider.dump(user), HTTPStatus.CREATED


class UserFindResource(Resource):
    @jwt_required
    def get(self, name):

        required_user = User.get_by_username(name)
        user = User.get_by_id(get_jwt_identity())

        if user is None or required_user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        if user.is_admin:
            return user_schema.dump(required_user), HTTPStatus.OK

        else:
            return user_schema_outsider.dump(required_user), HTTPStatus.OK

    @jwt_required
    def delete(self, name):
        user = User.get_by_id(get_jwt_identity())

        json_data = request.get_json()

        password = json_data.get('password')

        required_user = User.get_by_username(name)

        if user.is_admin:

            if required_user is not None and check_admin(password):
                required_user.delete()
                return {"message": 'User successfully deleted'}, HTTPStatus.OK
            else:
                return {"message": 'User does not exist or admin password is wrong'}, HTTPStatus.BAD_REQUEST
        else:
            return {'message': 'Admins only'}, HTTPStatus.FORBIDDEN


class MeResource(Resource):

    @jwt_required
    def get(self):
        user = User.get_by_id(get_jwt_identity())

        return UserInfoSchema().dump(user)

