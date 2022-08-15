import jwt
import calendar
import datetime

from flask_restx import abort

from constsnts import SECRET_KEY, ALGORITM
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_token(self, username, password, is_refresh=False):
        user = self.user_service.get_user_by_username(username)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not self.user_service.compare_passwords(password, user.password):
                raise Exception("Пароли не совпадают")

        data = {
            'username': user.username,
            'role': user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITM)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 201

    def approve_refresh_token(self, refresh_token):

        data = jwt.decode(jwt=refresh_token, key=SECRET_KEY, algorithms=[ALGORITM])
        username = data['username']

        user = self.user_service.get_user_by_username(username)

        if not user:
            raise Exception()

        return self.generate_token(user.username, user.password, is_refresh=True)
