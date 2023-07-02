from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, BigInteger, VARCHAR, Text, SmallInteger, Integer, Double, DateTime

from sqldaogenerator.entity.General import General
from sqldaogenerator.entity.Page import Page
from sqldaogenerator.entity.base import Base


class SampleE(Base):
    __tablename__ = 't_sample'

    id = Column(BigInteger, autoincrement=True, primary_key=True, comment='主鍵')
    col_var = Column(VARCHAR, primary_key=True, comment='字串')
    col_text = Column(Text, primary_key=True, comment='長字串')
    col_tinyint = Column(SmallInteger, primary_key=True, comment='微整數')
    col_int = Column(Integer, primary_key=True, comment='整數')
    col_double = Column(Double, primary_key=True, comment='浮點數')
    col_datetime = Column(DateTime, primary_key=True, comment='時間')


@dataclass
class Sample(General, Page):
    col_var: str = None
    col_var_in: list[str] = None
    col_text: str = None
    col_text_in: list[str] = None
    col_tinyint: int = None
    col_tinyint_in: list[int] = None
    col_tinyint_gte: int = None
    col_tinyint_lte: int = None
    col_int: int = None
    col_int_in: list[int] = None
    col_int_gte: int = None
    col_int_lte: int = None
    col_double: float = None
    col_double_in: list[float] = None
    col_double_gte: float = None
    col_double_lte: float = None
    col_datetime: datetime | str = None
    col_datetime_start: datetime | str = None
    col_datetime_end: datetime | str = None

    def equals_filters(self):
        return [(SampleE.id, self.id), (SampleE.col_var, self.col_var), (SampleE.col_text, self.col_text),
                (SampleE.col_tinyint, self.col_tinyint), (SampleE.col_int, self.col_int), (SampleE.col_double, self.col_double),
                (SampleE.col_datetime, self.col_datetime)]

    def in_filters(self):
        return [(SampleE.id, self.id_in), (SampleE.col_var, self.col_var_in), (SampleE.col_text, self.col_text_in),
                (SampleE.col_tinyint, self.col_tinyint_in), (SampleE.col_int, self.col_int_in),
                (SampleE.col_double, self.col_double_in)]

    def gte_filters(self):
        return [(SampleE.id, self.id_gte), (SampleE.col_tinyint, self.col_tinyint_gte), (SampleE.col_int, self.col_int_gte),
                (SampleE.col_double, self.col_double_gte)]

    def lte_filters(self):
        return [(SampleE.id, self.id_lte), (SampleE.col_tinyint, self.col_tinyint_lte), (SampleE.col_int, self.col_int_lte),
                (SampleE.col_double, self.col_double_lte)]

    def date_filters(self):
        return [(SampleE.col_datetime, (self.col_datetime_start, self.col_datetime_end))]
