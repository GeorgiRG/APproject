from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.workspace import Workspace
from models.user import User


class WorkspaceResource(Resource):
    def get(self):
        workspace_list = Workspace.get_all()
        info = []
        for workspace in workspace_list:
            info.append(workspace.info())

        return {'info': info}, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()
        user = User.get_by_id(user_id=get_jwt_identity())

        if user.is_admin:
            workspace = Workspace(workspace_number=json_data['workspace_number'],
                                  turkuamk_only=json_data['turkuamk_only'],
                                  available_space=json_data['available_space']
                                  )
            workspace.save()
            return workspace.info(), HTTPStatus.CREATED
        else:
            return {'message': 'User is not admin'}, HTTPStatus.FORBIDDEN


class WorkspaceUpdateResource(Resource):
    @jwt_required
    def put(self, workspace_number):
        json_data = request.get_json()
        user = User.get_by_id(user_id=get_jwt_identity())

        workspace = Workspace.get_by_number(workspace_number)
        if user.is_admin:
            workspace.workspace_number = json_data['workspace_number']
            workspace.turkuamk_only = json_data['turkuamk_only']
            workspace.available_space = json_data['available_space']

            workspace.save()
            return workspace.info(), HTTPStatus.CREATED
        else:
            return {'message': 'User is not admin'}, HTTPStatus.FORBIDDEN

    @jwt_required
    def delete(self, workspace_number):
        user = User.get_by_id(user_id=get_jwt_identity())
        workspace = Workspace.get_by_number(workspace_number)

        if user.is_admin:
            workspace.delete()
            return {'message': "Workspace was deleted"}, HTTPStatus.OK
        else:
            return {'message': 'User is not admin'}, HTTPStatus.FORBIDDEN

