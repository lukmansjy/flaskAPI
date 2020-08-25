from flask import jsonify, Blueprint, abort
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)

import models

message_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'published_at': fields.String
}

class UserBase(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'content',
            required=True,
            help='Kontent wajib ada',
            location=['form', 'json']
        )
        super().__init__()


class MessageList(UserBase):
    def get(self):
        messages = [marshal(message, message_fields) for message in models.Message.select()]
        return jsonify(messages)

    @jwt_required
    def post(self):
        args = self.reqparse.parse_args()
        current_user = get_jwt_identity()
        user = models.User.select().where( models.User.username == current_user ).get()
        message = models.Message.create(
            user_id=user.id,
            content=args.get('content')
        )
        return marshal(message, message_fields)


class Message(UserBase):
    def get(self, id):
        try:
            message = models.Message.get_by_id(id)
        except models.Message.DoesNotExist:
            abort(404)
        else:
            return marshal(message, message_fields)

    @jwt_required
    def put(self, id):
        args = self.reqparse.parse_args()
        try:
            message = models.Message.get_by_id(id)
        except models.Message.DoesNotExist:
            abort(404)
        else:
            current_user = get_jwt_identity()
            user = models.User.select().where( models.User.username == current_user ).get()
            if user == message.user_id:
                models.Message.update(content=args.get('content')).where(models.Message.id == id).execute()
                return {
                    'message': 'update success'
                }
            else:
                return {
                    'message': 'Kamu tidak dapat edit message ini'
                }, 403

    @jwt_required
    def delete(self, id):
        try:
            message = models.Message.get_by_id(id)
        except models.Message.DoesNotExist:
            abort(404)
        else:
            current_user = get_jwt_identity()
            user = models.User.select().where( models.User.username == current_user ).get()
            if user == message.user_id:
                models.Message.delete().where(models.Message.id == id).execute()
                return {
                    'message': 'delete success'
                }
            else:
                return {
                    'message': 'Kamu tidak dapat menghapus message ini'
                }, 403


messages_api = Blueprint('resources.messages', __name__)
api = Api(messages_api)
api.add_resource(MessageList, '/messages', endpoint='messages')
api.add_resource(Message, '/message/<int:id>', endpoint='message')