from flask_restful import Resource

from database.db_working import *
from .parsers import *
from .utils import *
from .validators import validate_api_key, validate_complete_data


class Good(Resource):

    def get(self):
        data = get_goods_parser.parse_args()
        user = validate_api_key(data['username'], data['API_key'])
        goods = get_goods(user, data['status'])
        response_body = [good.as_dict() for good in goods]
        return {'goods': response_body}

    def put(self):
        data = goods_create_parser.parse_args()
        user = validate_api_key(data['username'], data['API_key'])
        create_goods(user, data['goods'])

        return '', 201

    def delete(self):
        data = delete_goods_parser.parse_args()
        user = validate_api_key(data['username'], data['API_key'])
        validated_data = validate_delete_data(user, data['goods'])
        delete_goods(validated_data)

        return '', 204

    def patch(self):
        data = change_goods_parser.parse_args()
        user = validate_api_key(data['username'], data['API_key'])
        validated_data = validate_change_data(user, data)
        update_good(data['good_id'], validated_data)

        return '', 200

    def post(self):
        data = complete_goods_parser.parse_args()
        user = validate_api_key(data['username'], data['API_key'])
        validated_data = validate_complete_data(user, data['goods'])
        complete_goods(validated_data)

        return ''


class Register(Resource):
    def post(self):
        register_data = register_parser.parse_args()

        salt, pswd_key, api_secret, api_secret_key = generate_secure_data(register_data['password'])
        create_user(usrnm=register_data['username'],
                    salt=salt,
                    pswd_key=pswd_key,
                    as_key=api_secret_key)

        return {'Your API_key': api_secret}


class RebuildAPIKey(Resource):
    def post(self):
        auth_data = auth_parser.parse_args()
        user = validate_auth_data(auth_data)
        api_secret, api_secret_key = generate_api_secret(user.salt)
        update_api_secret(user.user_id, api_secret_key)
        return {'Your API_key': api_secret}

