from .resources import Good, Register, RebuildAPIKey

from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app)

api.add_resource(Good, '/api/goods/')
api.add_resource(Register, '/api/register/')
api.add_resource(RebuildAPIKey, '/api/new_api_key/')
