from sqlalchemy import Column, BigInteger, VARCHAR, Text, SmallInteger, Integer, Double, DateTime

from sample.entity.SampleCriterion import SampleCriterion
from sqldaogenerator.entity.base import Base

"""This file is generated by sqldao-generator; don't modify anything. If you need to do it, you should create another class."""


class Sample(Base):
    __tablename__ = 't_sample'

    col_datetime = Column(DateTime, comment='時間')
    col_double = Column(Double, comment='浮點數')
    col_int = Column(Integer, comment='整數')
    col_text = Column(Text, comment='長字串')
    col_tinyint = Column(SmallInteger, comment='微整數')
    col_var = Column(VARCHAR, comment='字串')
    id = Column(BigInteger, autoincrement=True, primary_key=True, comment='主鍵')

    @staticmethod
    def equals_filters(criterion: SampleCriterion):
        return [(Sample.col_datetime, criterion.col_datetime),
                (Sample.col_double, criterion.col_double),
                (Sample.col_int, criterion.col_int),
                (Sample.col_text, criterion.col_text),
                (Sample.col_tinyint, criterion.col_tinyint),
                (Sample.col_var, criterion.col_var),
                (Sample.id, criterion.id)]

    @staticmethod
    def in_filters(criterion: SampleCriterion):
        return [(Sample.col_datetime, criterion.col_datetime_in),
                (Sample.col_double, criterion.col_double_in),
                (Sample.col_int, criterion.col_int_in),
                (Sample.col_text, criterion.col_text_in),
                (Sample.col_tinyint, criterion.col_tinyint_in),
                (Sample.col_var, criterion.col_var_in),
                (Sample.id, criterion.id_in)]

    @staticmethod
    def gte_filters(criterion: SampleCriterion):
        return [(Sample.col_double, criterion.col_double_gte),
                (Sample.col_int, criterion.col_int_gte),
                (Sample.col_tinyint, criterion.col_tinyint_gte),
                (Sample.id, criterion.id_gte)]

    @staticmethod
    def lte_filters(criterion: SampleCriterion):
        return [(Sample.col_double, criterion.col_double_lte),
                (Sample.col_int, criterion.col_int_lte),
                (Sample.col_tinyint, criterion.col_tinyint_lte),
                (Sample.id, criterion.id_lte)]

    @staticmethod
    def date_filters(criterion: SampleCriterion):
        return [(Sample.col_datetime, (criterion.col_datetime_start, criterion.col_datetime_end))]
