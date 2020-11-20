from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from utils import check_timeframes


from models.reservation import Reservation
from models.user import User
from models.workspace import Workspace
from models.timeframes import Timeframes

from datetime import datetime, timedelta

from schemas.reservation import ReservationSchema


class ReservationResource(Resource):

    @jwt_required
    def get(self):
        user = User.get_by_id(user_id=get_jwt_identity())

        if user.is_admin:
            return ReservationSchema(many=True).dump(Reservation.show_all()), HTTPStatus.OK

        else:
            if Reservation.show_mine(user.username):
                return ReservationSchema(many=True).dump(Reservation.show_mine(user.username)), HTTPStatus.OK
            else:
                return {"message": 'You have no reservations'}, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()

        data, errors = ReservationSchema().load(json_data)
        current_user = User.get_by_id(user_id=get_jwt_identity())
        current_workspace = Workspace.get_by_number(data.get('workspace_number'))

        # check duration format

        if "minutes" in data.get('duration'):
            increase = timedelta(minutes=int(''.join(filter(str.isdigit, data.get('duration')))))
        elif "hours" in json_data['duration']:
            increase = timedelta(hours=int(''.join(filter(str.isdigit, data.get('duration')))))
        else:
            return {"message": 'Wrong format, correct example - [10 hours]'}, HTTPStatus.BAD_REQUEST

        # assign start and end time

        ending_time = data.get('start_time') + increase

        check_timeframes_result = check_timeframes(data.get('starting_time'), ending_time,
                                                   current_workspace.workspace_number)

        # check if it can fit all

        if json_data['attendees'] >= current_workspace.available_space:
            return {"message": 'Not enough space'}, HTTPStatus.BAD_REQUEST

        # check if the workspace is available

        if current_workspace.turkuamk_only is True and current_user.is_turkuamk is False:
            return {"message": 'This workspace is only for TurkuAMK users'}, HTTPStatus.BAD_REQUEST

        if check_timeframes_result is not None:
            return {"message": check_timeframes_result}, HTTPStatus.BAD_REQUEST
        else:
            new_reservation = Reservation(**data)

            new_timeframe = Timeframes(start_time=data.get('start_time'),
                                       end_time=ending_time,
                                       workspace=current_workspace.workspace_number,
                                       user_id=current_user.id
                                       )

            new_reservation.save()
            new_timeframe.save()

            return ReservationSchema().dump(new_reservation), HTTPStatus.OK

    @jwt_required
    def put(self):
        user = User.get_by_id(user_id=get_jwt_identity())
        json_data = request.get_json()
        reservation = Reservation.find_by_workspace(json_data['workspace'])
        current_workspace = Workspace.get_by_number(json_data['workspace'])
        previous_timeframe = Timeframes.get_for_this_workspace(current_workspace.workspace_number, user.id)

        if "minutes" in json_data['duration']:
            increase = timedelta(minutes=int(''.join(filter(str.isdigit, json_data['duration']))))
        elif "hours" in json_data['duration']:
            increase = timedelta(hours=int(''.join(filter(str.isdigit, json_data['duration']))))
        else:
            return {"message": 'Wrong format'}, HTTPStatus.BAD_REQUEST

        starting_time = datetime.strptime(json_data['start_time'], "%d/%m/%Y %H:%M")
        ending_time = datetime.strptime(json_data['start_time'], "%d/%m/%Y %H:%M") + increase
        check_timeframes_result = check_timeframes(starting_time, ending_time, current_workspace.workspace_number)

        if check_timeframes_result is str:
            return {"message": check_timeframes_result}, HTTPStatus.BAD_REQUEST
        elif reservation.user_id != user.id:
            return {"message": "No such reservation"}, HTTPStatus.BAD_REQUEST
        else:
            reservation.start_time = starting_time
            reservation.end_time = ending_time
            reservation.duration = increase
            reservation.reserved_by = user.username
            reservation.workspace = current_workspace.workspace_number

            new_timeframe = Timeframes(start_time=starting_time,
                                       end_time=ending_time,
                                       workspace=current_workspace.workspace_number,
                                       user_id=user.id
                                       )

            reservation.save()
            new_timeframe.save()
            previous_timeframe.delete()

    @jwt_required
    def delete(self):
        user = User.get_by_id(user_id=get_jwt_identity())
        json_data = request.get_json()
        reservation = Reservation.find_by_workspace(json_data['workspace'])
        current_workspace = Workspace.get_by_number(json_data['workspace'])
        timeframe = Timeframes.get_for_this_workspace(current_workspace.workspace_number, user.id)

        if reservation is not None:
            reservation.delete()
        else:
            return {"message": "Already deleted or it doesn't exist"}, HTTPStatus.NOT_FOUND

        if timeframe is not None:
            timeframe.delete()

        return {}, HTTPStatus.NO_CONTENT







