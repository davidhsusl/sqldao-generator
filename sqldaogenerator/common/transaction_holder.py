import threading

from sqlalchemy.orm import Session, sessionmaker

from sqldaogenerator.logger.logger import info

# Create a thread-local object
transaction_thread = threading.local()
session_maker: sessionmaker


def register_session_maker(session: sessionmaker):
    global session_maker
    session_maker = session


def get_transaction() -> Session:
    if hasattr(transaction_thread, 'is_exists') and transaction_thread.is_exists:
        return transaction_thread.session
    else:
        raise LookupError('No existing transaction.')


def transactional(func):
    def wrapper(*args, **kwargs):
        if hasattr(transaction_thread, 'is_exists') and transaction_thread.is_exists:
            info('Participating in an existing transaction.')
            result = func(*args, **kwargs)
        else:
            info('Creating a new transaction.')
            with session_maker() as session:
                transaction_thread.is_exists = True
                transaction_thread.session = session
                result = func(*args, **kwargs)
                session.commit()
                transaction_thread.is_exists = False
        return result

    return wrapper
