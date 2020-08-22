from flask import Blueprint, jsonify
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api, reqparse, fields, marshal

import models

user_fields = {
    'username': fields.String
}

bcrypt = Bcrypt()

class UserRegister(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='username required',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='password required',
            location=['form', 'json']
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        username = args.get('username')
        password =  bcrypt.generate_password_hash( args.get('password') )
        
        # Register User
        try:
            # Cek user sudah ada atau belum, jika tidak ada maka ke except
            models.User.select().where( models.User.username == username ).get()
        except models.User.DoesNotExist:
            # Insert user ke DB
            user = models.User.create(
                username = username,
                password = password
            )
            return marshal(user, user_fields)
        else:
            # Return mengguanakan error code
            return {
                'message': 'Username sudah terdaftar'
            }, 401


class UserLogin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='username required',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='password required',
            location=['form', 'json']
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        username = args.get('username')
        password = args.get('password')

        try:
            user = models.User.get( models.User.username == username)
        except models.User.DoesNotExist:
            return {
                'message': 'Username atau password salah'
            }, 401
        else:
            if bcrypt.check_password_hash( user.password, password) :
                return {
                    'message': 'success'
                }
            else:
                return {
                    'message': 'Password salah'
                }, 401


user_api = Blueprint('resources.users', __name__)
api = Api(user_api)
api.add_resource(UserRegister, '/user/register', endpoint='register')
api.add_resource(UserLogin, '/user/login', endpoint='login')