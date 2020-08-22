from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)

from resources.messages import messages_api
from resources.users import user_api

import models

app = Flask(__name__)
app.register_blueprint(messages_api, url_prefix='/api/v1')
app.register_blueprint(user_api, url_prefix='/api/v1')

app.config['JWT_SECRET_KEY'] = 'kuncirahasia123456'
jwt = JWTManager(app)

if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)
