from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db, jwt

from resources.token import TokenResource, RefreshResource, RevokeResource, black_list
from resources.user import UserResource, MeResource, UserFindResource, UserDeleteResource
from resources.reservation import ReservationResource
from resources.workspace import WorkspaceResource, WorkspaceUpdateResource


def create_app():
    app = Flask('APproject')
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list


def register_resources(app):
    api = Api(app)

    api.add_resource(UserResource, '/users')
    api.add_resource(UserFindResource, '/users/find/<string:name>')
    api.add_resource(UserDeleteResource, '/users/delete/<string:name>')

    api.add_resource(MeResource, '/me')

    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')

    api.add_resource(ReservationResource, '/reservations')

    api.add_resource(WorkspaceResource, '/workspaces')
    api.add_resource(WorkspaceUpdateResource, '/workspaces/<string:workspace_number>')


application = create_app()
application.run()
