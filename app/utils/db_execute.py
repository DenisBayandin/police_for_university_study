from settings import db_connection

from .errors import DbExecuteException


def db_execute():
    def decorator(func):
        def wrapper(*args, **kwargs):
            cur = db_connection.cursor()
            db_action = func(*args, **kwargs)
            try:
                cur.execute(db_action)
            except Exception as e:
                db_connection.rollback()
                raise DbExecuteException(e)
            db_connection.commit()
            cur.close()
        return wrapper
    return decorator


def list_db_execute():
    def decorator(func):
        def wrapper(*args, **kwargs):
            cur = db_connection.cursor()
            db_action = func(*args, **kwargs)
            try:
                cur.execute(db_action)
                result = cur.fetchall()
            except Exception as e:
                db_connection.rollback()
                print(f"Error: {e}")
                result = None
            cur.close()
            return result
        return wrapper
    return decorator
