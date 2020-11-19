from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from utils import hash_password, check_admin, check_email
from models.user import User
from models.reservation import Reservation


class UserResource(Resource):
    def post(self):
        json_data = request.get_json()

        username = json_data.get("username")
        email = json_data.get("email")
        non_hash_password = json_data.get("password")
        adm_pass = json_data.get("admin_pass")

        if User.get_by_username(username):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(email):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        password = hash_password(non_hash_password)

        if check_admin(adm_pass) and check_email(email):
            user = User(
                username=username,
                email=email,
                password=password,
                is_turkuamk=True,
                is_admin=True
            )
        elif check_email(email):
            user = User(
                username=username,
                email=email,
                password=password,
                is_turkuamk=True
            )
        else:
            user = User(
                username=username,
                email=email,
                password=password
            )

        user.save()

        if user.is_admin:
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'admin_privileges': user.is_admin
            }
        else:
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }

        return data, HTTPStatus.CREATED

    @jwt_required
    def get(self):

        json_data = request.get_json()
        required_user = User.get_by_username(json_data["username"])
        user = User.get_by_id(get_jwt_identity())

        if user is None or required_user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        if user.is_admin:
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_turkuamk': user.is_turkuamk,
                'is_admin': user.is_admin
            }
        else:
            data = {
                'id': user.id,
                'username': user.username,
                'is_turkuamk': user.is_turkuamk
            }
        return data, HTTPStatus.OK


class MeResource(Resource):

    @jwt_required
    def get(self):
        user = User.get_by_id(get_jwt_identity())
        reservations = Reservation.show_mine(user.username)
        reservation_data = []
        for reservation in reservations:
            reservation_data.append(reservation.info())
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_turkuamk': user.is_turkuamk,
            'is_admin': user.is_admin,
            'my_reservations': reservation_data
        }

        return data, HTTPStatus.OK


class AdminResource(Resource):

    @jwt_required
    def get(self):
        user = User.get_by_id(user_id=get_jwt_identity())

        if user.is_admin:
            json_data = request.get_json()

            username = json_data.get('username')

            reservations = Reservation.show_mine(username)
            reservation_data = []
            for reservation in reservations:
                reservation_data.append(reservation.info())

            if username:
                required_user = User.get_by_username(username)

                data = {
                    'id': required_user.id,
                    'username': required_user.username,
                    'email': required_user.email,
                    'reservations': reservation_data
                }
                return data,  HTTPStatus.OK
        else:
            return {'message': 'User is not admin'}, HTTPStatus.FORBIDDEN

    @jwt_required
    def delete(self):
        user = User.get_by_id(get_jwt_identity())

        json_data = request.get_json()

        username = json_data.get('username')
        password = json_data.get('password')
        required_user = User.get_by_username(username)

        if user.is_admin:

            if required_user is not None and check_admin(password):
                required_user.delete()
                return {"message": 'User successfully deleted'}, HTTPStatus.OK
            else:
                return {"message": 'User does not exist or password is wrong'}, HTTPStatus.BAD_REQUEST
        else:
            return {'message': 'User is not admin'}, HTTPStatus.FORBIDDEN
