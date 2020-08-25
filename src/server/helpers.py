from contextlib import contextmanager
from functools import wraps
import logging
from sqlalchemy.orm import sessionmaker
from config import engine

LOGGER = logging.getLogger(__file__)

@contextmanager
def create_session():
    """
    Simple context manager that will create and destroy a session
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def provide_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_arg_name = "session"
        func_params = func.__code__.co_varnames
        if session_arg_name not in func_params:
            logging.warn("No `session` parameter exists for this function.  Doing nothing.")
            return func(*args, **kwargs)
        in_args = session_arg_name in func_params and func_params.index(session_arg_name) < len(args)
        in_kwargs = session_arg_name in kwargs
        if in_args or in_kwargs:
            return func(*args, **kwargs)
        else:
            with create_session() as session:
                return func(*args, session=session, **kwargs)
    return wrapper