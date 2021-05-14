from database.db_working import is_user_exist_by_username, is_good_exist
from database.tables import *
from flask_restful import abort
from hashlib import pbkdf2_hmac


def price(value):
    # Валидация цены
    if value <= 0 or value > 10**18:
        raise ValueError('Цена должна быть положительным числом меньшим 10^18')
    return value


def pswd(value):
    # Валидация длины пароля
    if len(value) < 8:
        raise ValueError('Пароль должен быть не короче 8 символов')
    return value


def usrnm(value):
    # Валидвция уникальности юзернейма
    user = is_user_exist_by_username(value)
    if user:
        raise ValueError('Пользователь с таким юзернеймом уже существует')
    return value


def validate_api_key(username, API_key):
    user = is_user_exist_by_username(username)
    if user:

        api_secret_key = pbkdf2_hmac(
            hash_name='sha256',
            password=API_key.encode('utf-8'),
            salt=user.salt,
            iterations=100000)

        if api_secret_key != user.api_secret:
            abort(400, message='Неверный API_key')

        return user

    abort(404, message='Такого пользователя не существует')


def validate_complete_data(user, data):

    for item in data:
        try:
            good = is_good_exist(item['good_id'])
            if not good:
                abort(404, message=f'Покупка с ID {item["good_id"]}: не существует')

            elif good.user_id != user.user_id:
                abort(400, message=f'Покупка с ID {good.good_id}: принадлежит другому пользователю')

            elif good.status != GoodStatus.in_progress:
                abort(400, message=f'Покупка с ID {good.good_id}: уже завершена')

            elif not isinstance(item['price'], float) or item['price'] <= 0 or item['price'] > 10**18:
                abort(400, message=f'Покупка с ID {good.good_id}: цена должна быть положительным float числом меншим '
                                   f'10^18')
        except KeyError:
            abort(400, message='Отсутсвует необходимый ключ')

    return data


def validate_delete_data(user, data):

    for item in data:
        good = is_good_exist(item)
        if not good:
            abort(404, message=f'Покупка с ID {item}: не существует')

        elif good.user_id != user.user_id:
            abort(400, message=f'Покупка с ID {good.good_id}: принадлежит другому пользователю')

    return data


def validate_change_data(user, data):
    output = {}
    try:
        good = is_good_exist(data['good_id'])
        if not good:
            abort(404, message=f'Покупки не существует')

        elif good.user_id != user.user_id:
            abort(400, message=f'Покупка принадлежит другому пользователю')

        elif not (data['price'] is None):
            if good.status == GoodStatus.in_progress:
                abort(400, message=f'Цену можно менять только у завершенных покупок')
            elif data['price'] <= 0 or data['price'] > 10**18:
                abort(400, message=f'Цена должна быть положительным float числом меншим 10^18')
            else:
                output['price'] = int(data['price']*100)

        if not (data['text'] is None):
            output['text'] = data['text']

    except ValueError:
        abort(400, message='Отсутсвует необходимый ключ "good_id"')

    if output:
        return output
    else:
        abort(400, message='Отсутсвует валидная информация для изменения')


def validate_auth_data(data):
    user = is_user_exist_by_username(data['username'])
    if user:

        pswd_key = pbkdf2_hmac(
            hash_name='sha256',
            password=data['password'].encode('utf-8'),
            salt=user.salt,
            iterations=100000)

        if pswd_key != user.password:
            abort(400, message='Неверный пароль')

        return user

    abort(404, message='Такого пользователя не существует')


