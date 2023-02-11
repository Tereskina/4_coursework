from flask import request
from flask_restx import Namespace, Resource
from project.container import user_service
from project.setup.api.models import user

api = Namespace('user')


@api.route("/")
class UserView(Resource):
    @api.marshal_with(user, code=200, description='OK')
    def get(self):
        """
         Получает информацию о пользователе (его профиль)
        """
        token = request.headers["Authorization"].split("Bearer ")[-1]
        return user_service.get_user_by_token(token)


    @api.marshal_with(user, code=200, description='OK')
    def patch(self):
        """изменить информацию пользователя."""
        token = request.headers["Authorization"].split("Bearer ")[-1]
        data = request.get_json()

        return user_service.update_user(data=data, token=token)


@api.route('/password/')
class LoginView(Resource):
    @api.marshal_with(user, code=200, description='OK')
    def put(self):
        """ Обновление пароля пользователя"""
        data = request.json
        token = request.headers["Authorization"].split("Bearer ")[-1]

        return user_service.update_password(data=data, token=token)

