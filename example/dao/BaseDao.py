"""This file is generated by sqldao-generator; don't modify anything"""
from example.dao.Datasource import datasource, Datasource


class BaseDao:
    datasource: Datasource

    def __init__(self):
        self.datasource = datasource

    def get_transaction(self):
        return self.datasource.transactionManager.get_transaction()

    def new_transaction(self):
        return self.datasource.transactionManager.new_transaction()
