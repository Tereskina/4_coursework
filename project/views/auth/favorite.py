from flask import request
from flask_restx import Namespace, Resource

from project.container import favorite_service

from project.models import MovieSchema
from project.tools.security import decode_token

api = Namespace('favorites')


@api.route('/movies/')
class FavouritesViews(Resource):
    @api.doc(description='Избранное пользователя')
    @api.response(200, 'Добавлено')
    @api.response(404, 'Нет такого фильма')
    def get(self):
        rs = favorite_service.get_user_favorites()
        res = MovieSchema(many=True).dump(rs)
        return res, 200



@api.route('/movies/<int:movie_id>/')
class FavouriteView(Resource):
    @api.doc(description='Добавляет в избранное')
    def post(self, movie_id):

        # Передаем токен пользователя
        token = request.headers["Authorization"].split("Bearer ")[-1]

        # Добавляем фильм в избранное
        return favorite_service.add_favourite(token, movie_id)

# Удаление из избранного не работает
    @api.doc(description='Удаляет из избранного')
    def delete(self, movie_id):
        # Передаем токен пользователя
        token = request.headers["Authorization"].split("Bearer ")[-1]

        favorite_service.delete_favorite(movie_id)
        return "", 200
