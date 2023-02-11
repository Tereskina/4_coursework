from marshmallow import Schema, fields
from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from project.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


class GenreSchema(Schema):
    name = fields.Str()


class Director(models.Base):
    __tablename__ = 'directors'

    name = Column(String(100), unique=True, nullable=False)


class DirectorSchema(Schema):
    name = fields.Str()


class Movie(models.Base):
    __tablename__ = 'movies'

    title = Column(String(255))
    description = Column(String(255))
    trailer = Column(String(255))
    year = Column(Integer)
    rating = Column(Float)
    genre_id = Column(Integer, ForeignKey("genres.id"))
    genre = relationship("Genre")
    director_id = Column(Integer, ForeignKey("directors.id"))
    director = relationship("Director")


class MovieSchema(Schema):

    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()
    genre = fields.Pluck(GenreSchema, 'name')
    director = fields.Pluck(DirectorSchema, 'name')

class User(models.Base):
    __tablename__ = 'users'

    email = Column(String(20), unique=True, nullable=False)
    name = Column(String(20))
    surname = Column(String(20))
    password = Column(String(10), nullable=False)
    favorite_genre = Column(Integer(), ForeignKey("genres.id"))
    genre = relationship("Genre")


class UserSchema(Schema):
    email = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    password = fields.Str()
    favorite_genre = fields.Int()


class Favorite(models.Base):
    __tablename__ = 'favorites'

    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    user = relationship("User")
    movie = relationship("Movie")


class FavoriteSchema(Schema):
    user_id = fields.Int()
    movie_id = fields.Int()
    user = fields.Pluck(UserSchema, 'name')
    movie = fields.Pluck(MovieSchema, 'title')
