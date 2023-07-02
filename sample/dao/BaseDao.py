from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqldaogenerator.common.transaction_holder import transaction
from sqldaogenerator.entity.General import General
from sqldaogenerator.entity.base import Base


class BaseDao:

    def __init__(self):
        user = 'daniel'
        password = '0614'
        host = 'localhost'
        port = '3306'
        dbname = 'database_test'
        connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}"
        self.engine = create_engine(connection_string, echo=True, pool_recycle=270)
        self.Session = sessionmaker(bind=self.engine)
        transaction.Session = self.Session

    def set_not_none(self, entity: Base, model: General, *criterion: str):
        for value in criterion:
            if value is not None:
                exec(f"entity.{value}=model.{value}")
