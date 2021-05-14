from datetime import datetime

from database.database import Session
from database import tables


def create_goods(user, goods):
    session = Session()

    for good in goods:
        instance = tables.Good(user_id=user.user_id,
                               text=good)
        session.add(instance)


    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_goods(user, status):
    session = Session()
    if status == 'all':
        goods = session.query(tables.Good).filter(tables.Good.user_id == user.user_id).all()
        session.close()
        return goods

    goods = session.query(tables.Good).filter(tables.Good.user_id == user.user_id) \
        .filter(tables.Good.status == tables.GoodStatus[status]).all()

    session.close()

    return goods


def is_good_exist(good_id):
    session = Session()
    good = session.query(tables.Good).filter(tables.Good.good_id == good_id).first()
    session.close()
    if good:
        return good
    return False


def complete_goods(data):
    session = Session()
    now = datetime.utcnow()
    for item in data:
        session.query(tables.Good).filter(tables.Good.good_id == item['good_id']).update(
            {'status': tables.GoodStatus.complete,
             'complete_date': now,
             'price': int(item['price'] * 100)})
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def delete_goods(goods):
    session = Session()

    session.query(tables.Good).filter(tables.Good.good_id.in_(goods)).delete()
    session.commit()
    session.close()


def update_good(good_id, data):
    session = Session()
    try:
        session.query(tables.Good).filter(tables.Good.good_id == good_id).update(data)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
