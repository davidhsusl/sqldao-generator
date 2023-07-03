from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy import Column

from sqldaogenerator.entity.General import General
from sqldaogenerator.entity.base import Base


@dataclass
class Criterion:
    equals_filters: list
    in_filters: list
    gte_filters: list
    lte_filters: list
    date_filters: list

    @staticmethod
    def builder():
        return CriterionBuilder()

    def to_list(self):
        return self.equals_filters + self.in_filters + self.gte_filters + self.lte_filters + self.date_filters


@dataclass
class CriterionBuilder:
    entity_attr: Base = None
    condition_attr: General = None
    equals_filters: list[any] = field(default_factory=list)
    in_filters: list[any] = field(default_factory=list)
    gte_filters: list[any] = field(default_factory=list)
    lte_filters: list[any] = field(default_factory=list)
    date_filters: list[any] = field(default_factory=list)

    def entity(self, entity):
        self.entity_attr = entity
        return self

    def condition(self, condition):
        self.condition_attr = condition
        return self

    def equals_filter(self, criterion: list[tuple[Column, any]]):
        for column, value in criterion:
            if value is not None and value != '':
                self.equals_filters.append(column == value)
        return self

    def in_filter(self, criterion: list[tuple[Column, list]]):
        for column, value in criterion:
            if value is not None and len(value) > 0:
                self.in_filters.append(column.in_(value))
        return self

    def gte_filter(self, criterion: list[tuple[Column, int | float]]):
        for column, value in criterion:
            if value is not None:
                self.gte_filters.append(column >= value)
        return self

    def lte_filter(self, criterion: list[tuple[Column, int | float]]):
        for column, value in criterion:
            if value is not None:
                self.lte_filters.append(column <= value)
        return self

    def date_filter(self, criterion: list[tuple[Column, tuple[datetime | str, datetime | str]]]):
        for column, value in criterion:
            begin_date, end_date = value
            if begin_date is not None and begin_date != '':
                self.date_filters.append(column >= begin_date)
            if end_date is not None and end_date != '':
                self.date_filters.append(column <= end_date)
        return self

    def build(self):
        return Criterion(self.equals_filters, self.in_filters, self.gte_filters, self.lte_filters, self.date_filters)
