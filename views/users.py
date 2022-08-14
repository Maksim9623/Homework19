from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('user')


@user_ns.route('/')
class UserView(Resource):
    def get(self):
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        req_json = request.json
        user_service.create_user(req_json)
        return "", 201


@user_ns.route('/<int:bid>')
class UserView(Resource):
    def delete(self, bid):
        user_service.delete(bid)
        return "", 204