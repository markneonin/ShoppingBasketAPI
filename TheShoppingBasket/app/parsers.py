from flask_restful import reqparse
from typing import List

from .validators import *

# Парсер для создания покупок
goods_create_parser = reqparse.RequestParser(bundle_errors=True)

goods_create_parser.add_argument(name='username', type=str, location='args', required=True)
goods_create_parser.add_argument(name='API_key', type=str, location='args', required=True)
goods_create_parser.add_argument('goods', type=str, action='append', required=True)


# Парсер для регистрации
register_parser = reqparse.RequestParser(bundle_errors=True)

register_parser.add_argument(name='username', type=usrnm, required=True)
register_parser.add_argument(name='password', type=pswd, required=True)


# Парсер для получения инфы о покупках
get_goods_parser = reqparse.RequestParser(bundle_errors=True)

get_goods_parser.add_argument(name='username', type=str, location='args', required=True)
get_goods_parser.add_argument(name='API_key', type=str, location='args', required=True)
get_goods_parser.add_argument(name='status', type=str, choices=['complete', 'all', 'in_progress'],
                              location='args', required=True)


# Парсер для завершения покупок
complete_goods_parser = reqparse.RequestParser(bundle_errors=True)

complete_goods_parser.add_argument(name='username', type=str, location='args', required=True)
complete_goods_parser.add_argument(name='API_key', type=str,location='args', required=True)
complete_goods_parser.add_argument(name='goods', type=dict, action='append', required=True)


# Парсер для удаления покупок
delete_goods_parser = reqparse.RequestParser(bundle_errors=True)
delete_goods_parser.add_argument(name='username', type=str, location='args', required=True)
delete_goods_parser.add_argument(name='API_key', type=str, location='args', required=True)
delete_goods_parser.add_argument(name='goods', type=int, action='append', required=True)


# Парсер для изменения покупки
change_goods_parser = reqparse.RequestParser(bundle_errors=True)

change_goods_parser.add_argument(name='username', type=str, location='args', required=True)
change_goods_parser.add_argument(name='API_key', type=str, location='args', required=True)
change_goods_parser.add_argument(name='good_id', type=int, required=True)
change_goods_parser.add_argument(name='text', type=str)
change_goods_parser.add_argument(name='price', type=float)


# Парсер для ребилда API_key
auth_parser = reqparse.RequestParser(bundle_errors=True)

auth_parser.add_argument(name='username', type=str, required=True)
auth_parser.add_argument(name='password', type=str, required=True)
