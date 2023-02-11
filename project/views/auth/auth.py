from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user

api = Namespace('auth')


@api.route("/register/")
class AuthView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def post(self):
        """Регистрация (создание нового) пользователя"""
        data = request.json

        if data.get('email') and data.get('password'):
            return user_service.create_user(email=data.get('email'), password=data.get('password')), 201
        else:
            return "Не получилось создать пользователя", 401


@api.route('/login/')
class AuthView(Resource):
    def post(self):
        """Идентификация пользователя (Login)"""
        data = request.json

        if data.get('email') and data.get('password'):
            return user_service.check(email=data.get('email'), password=data.get('password')), 200
        elif None in [data.get('email'), data.get("password")]:
            return "Нужно ввести email и пароль", 400
        else:
            return "Не получилось залогинить пользователя", 400

    def put(self):
        """
        Update tokens
        """
        data = request.json

        if data.get('access_token') and data.get('refresh_token'):
            return user_service.update_token(access_token=data.get('access_token'),
                                             refresh_token=data.get('refresh_token')), 200
        else:
            return "Не получилось обновить токены", 401
