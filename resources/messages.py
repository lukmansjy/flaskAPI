from flask import jsonify, Blueprint, abort
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)

import models

message_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'published_at': fields.String
}


class MessageList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'content',
            required=True,
            help='Kontent wajib ada',
            location=['form', 'json']
        )
        super().__init__()

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


class Message(Resource):
    def get(self, id):
        try:
            message = models.Message.get_by_id(id)
        except models.Message.DoesNotExist:
            abort(404)
        else:
            return marshal(message, message_fields)

messages_api = Blueprint('resources.messages', __name__)
api = Api(messages_api)
api.add_resource(MessageList, '/messages', endpoint='messages')
api.add_resource(Message, '/message/<int:id>', endpoint='message')