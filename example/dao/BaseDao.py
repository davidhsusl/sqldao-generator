"""
This file is generated by sqldao-generator; don't modify anything
"""
from typing import Type

from sqlalchemy import BinaryExpression

from sqldaogenerator.common.Criterion import Criterion
from example.dao.Datasource import datasource, Datasource


class BaseDao:
    datasource: Datasource

    def __init__(self):
        self.datasource = datasource

    def is_transaction_exists(self):
        return self.datasource.is_transaction_exists()

    def get_transaction(self):
        return self.datasource.get_transaction()

    def new_transaction(self):
        return self.datasource.new_transaction()

    @staticmethod
    def is_in_modules(expressions: list[BinaryExpression], *clss: type):
        modules = [cls.__module__ for cls in clss]
        return all(expression.left.entity_namespace.__module__ in modules for expression in expressions)

    @staticmethod
    def convert(entities: list, labels: list[str], cls: Type):
        new_entities = []
        for entity in entities:
            new_entity = cls()
            for i, label in enumerate(labels):
                setattr(new_entity, label, entity[i])
            new_entities.append(new_entity)
        return new_entities

    def get_query(self, criterion: Criterion, cls: Type):
        session = self.get_transaction()
        query_columns = []
        if criterion.columns:
            query_columns += criterion.columns
        if criterion.counts:
            query_columns += criterion.counts
        if criterion.maxes:
            query_columns += criterion.maxes
        if criterion.mines:
            query_columns += criterion.mines
        if criterion.sums:
            query_columns += criterion.sums
        if query_columns:
            query = session.query(*query_columns)
        else:
            query = session.query(cls)
        if criterion.distinct:
            query = query.distinct()
        query = query.filter(*criterion.filters)
        if criterion.groups:
            query = query.group_by(*criterion.groups)
        return query
