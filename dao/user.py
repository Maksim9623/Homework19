
from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def get_user_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def create_user(self, user):
        user_ent = User(**user)
        self.session.add(user_ent)
        self.session.commit()
        return user_ent

    def update(self, user):
        user = self.get_one(user.get("id"))
        user.name = user.get("username")
        user.password = user.get("password")
        user.role = user.get("role")

        self.session.add(user)
        self.session.commit()

    def get_one(self, bid):
        return self.session.query(User).get(bid)

    def delete(self, bid):
        user = self.get_one(bid)
        self.session.delete(user)
        self.session.commit()


