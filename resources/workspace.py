from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.workspace import Workspace
from models.user import User

from schemas.workspace import WorkspaceSchema


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
        data = WorkspaceSchema().load(json_data)

        if Workspace.get_by_number(data.get("workspace_number")):
            return {"message": "This workspace exists"}, HTTPStatus.BAD_REQUEST

        if user.is_admin:
            workspace = Workspace(**data)
            workspace.save()
            return WorkspaceSchema().dump(workspace), HTTPStatus.CREATED
        else:
            return {'message': 'User is not admin'}, HTTPStatus.FORBIDDEN


class WorkspaceUpdateResource(Resource):
    @jwt_required
    def put(self, workspace_number):
        json_data = request.get_json()
        user = User.get_by_id(user_id=get_jwt_identity())
        data = WorkspaceSchema().load(json_data)

        workspace = Workspace.get_by_number(workspace_number)
        if workspace is None:
            return {"message": "This workspace does not exist"}, HTTPStatus.BAD_REQUEST

        if user.is_admin:
            workspace.workspace_number = data.get('workspace_number')
            workspace.turkuamk_only = data.get('turkuamk_only')
            workspace.available_space = data.get('available_space')

            workspace.save()
            return WorkspaceSchema().dump(workspace), HTTPStatus.OK
        else:
            return {'message': 'User is not admin'}, HTTPStatus.FORBIDDEN

    @jwt_required
    def delete(self, workspace_number):
        user = User.get_by_id(user_id=get_jwt_identity())
        workspace = Workspace.get_by_number(workspace_number)

        if workspace is None:
            return {"message": "This workspace does not exist"}, HTTPStatus.BAD_REQUEST

        if user.is_admin:
            workspace.delete()
            return {'message': "Workspace was deleted"}, HTTPStatus.OK
        else:
            return {'message': 'User is not admin'}, HTTPStatus.FORBIDDEN

