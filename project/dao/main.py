from typing import Optional

from flask_sqlalchemy import BaseQuery

from project.dao.base import BaseDAO
from project.models import User, Genre, Director, Movie, Favorite


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def get_user_by_email(self, email: Optional[str]):
        """Получить пользователя по email"""
        stmt: BaseQuery = self._db_session.query(self.__model__)
        return stmt.filter(self.__model__.email == email).one()

    def create_user(self, email, password):
        user = User(
            email=email,
            password=password
        )
        try:
            self._db_session.add(
                user
            )
            self._db_session.commit()
            print("Пользователь добавился")
            return user

        except Exception as e:
            self._db_session.rollback()
            print(f"Не удалось создать пользователя\n{e}")


    def update_user(self, data, email):
        try:
            self._db_session.query(self.__model__).filter(self.__model__.email == email).update(data)
            self._db_session.commit()
            print("Обновление данных пользователя прошло успешно")

        except Exception as e:
            print(f"Ошибка обновления пользователя\n{e}")
            self._db_session.rollback()


class FavoritesDAO(BaseDAO[Favorite]):
    __model__ = Favorite

    def get_favorite(self, user_id, movie_id) -> list:
        """ Получить фильм из избранного """
        data = self._db_session.query(Favorite) \
            .filter(Favorite.user_id == user_id, Favorite.movie_id == movie_id) \
            .all()
        return data

    def get_user_favorites(self) -> list:
        """ Получает закладки у пользователя"""
        data = self._db_session.query(Movie).join(Favorite).all()
        return data

    def create(self, data: dict) -> object:
        """ Добавляет фильм в базу"""
        item = self.__model__(**data)
        self._db_session.add(item)
        self._db_session.commit()
        return item

    def delete(self, uid):
        item = self.__model__(uid)
        self._db_session.delete(item)
        self._db_session.commit()
