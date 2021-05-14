from database.database import Session
from database import tables


def create_user(usrnm, salt, pswd_key, as_key):
    session = Session()

    user = tables.User(username=usrnm,
                       salt=salt,
                       password=pswd_key,
                       api_secret=as_key)

    try:
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def is_user_exist_by_username(username):
    session = Session()
    user = session.query(tables.User).filter(tables.User.username == username).first()
    session.close()
    if user:
        return user
    else:
        return False


def update_api_secret(user_id, api_secret_key):
    session = Session()
    try:
        session.query(tables.User).filter(tables.User.user_id == user_id).update({'api_secret': api_secret_key})
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
