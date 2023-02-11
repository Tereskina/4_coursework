from typing import Optional

from project.dao import UsersDAO
from project.dao.main import User
from project.exceptions import ItemNotFound
from project.tools.security import generate_password_hash, generate_token, update_token, get_data_by_token


class UsersService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, status: Optional[str] = None, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page, status=status)

    def create_user(self, email: str, password: str):
        return self.dao.create_user(email=email, password=generate_password_hash(password))

    def get_user_by_email(self, email: str) -> User:
        return self.dao.get_user_by_email(email)

    def check(self, email: str, password: str):
        user = self.get_user_by_email(email)
        return generate_token(email=email, password=password, password_hash=user.password)

    def update_token(self, access_token, refresh_token):
        return update_token(refresh_token=refresh_token)

    def get_user_by_token(self, token):
        data = get_data_by_token(token)
        if data:
            # заблюрить пароль
            user = self.get_user_by_email(data.get("email"))
            user.password = "***"
            return user


    def update_user(self, data: str, token: str):
        user = get_data_by_token(token)
        if user:
            self.dao.update_user(data=data, email=user.get("email"))

            user = self.get_user_by_email(user.get("email"))
            user.password = "***"
            return user

    def update_password(self, data, token):

        if user := get_data_by_token(token):

            self.dao.update_user(
                data={
                    "password": generate_password_hash(data.get("new_password"))
                },
                email=user.get("email")
                )
            user = self.get_user_by_email(user.get("email"))
            user.password = "***"
            return user
