from enum import Enum


# from sqlalchemy import BigInteger, VARCHAR, Text, SmallInteger, Integer, Double, DateTime


class MySqlTypeEnum(Enum):
    BIGINT = 'BigInteger'
    VARCHAR = 'VARCHAR'
    TEXT = 'Text'
    TINYINT = 'SmallInteger'
    INT = 'Integer'
    DOUBLE = 'Double'
    DATETIME = 'DateTime'
