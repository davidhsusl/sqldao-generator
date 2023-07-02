import threading

from sqlalchemy.orm import Session

from sqldaogenerator.logger.logger import info

# Create a thread-local object
transaction = threading.local()
transaction.is_exists = False


def get_transaction() -> Session:
    if transaction.is_exists:
        return transaction.session
    else:
        raise LookupError('No existing transaction.')


def transactional(func):
    def wrapper(*args, **kwargs):
        if transaction.is_exists:
            info('Participating in an existing transaction.')
            result = func(*args, **kwargs)
        else:
            info('Creating a new transaction.')
            with transaction.Session() as session:
                transaction.is_exists = True
                transaction.session = session
                result = func(*args, **kwargs)
                session.commit()
                transaction.is_exists = False
        return result
    return wrapper
