import base64
import hashlib
import hmac

from dao.user import UserDAO
from constsnts import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_user_by_username(self, username):
        return self.dao.get_user_by_username(username)

    def hash_password(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )).decode('utf-8', 'ignore')

    def create_user(self, user):
        user['password'] = self.hash_password(user['password'])
        return self.dao.create_user(user)

    def compare_passwords(self, other_password, password_hash) -> bool:
        decode_digest = base64.b64decode(password_hash)
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hmac.compare_digest(decode_digest, hash_digest)

    def delete(self, rid):
        self.dao.delete(rid)



