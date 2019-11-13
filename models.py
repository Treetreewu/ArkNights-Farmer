"""
deprecated. Use `./config.json` to store data.
"""


import sqlite3
from sqlalchemy import Column, Integer, Boolean, String, create_engine, Enum
from sqlalchemy.ext.declarative import declarative_base


ModelBase = declarative_base()


class Device(ModelBase):
    serial_number = Column(String)
    status = Column(Integer)


if __name__ == '__main__':
    engine = create_engine("sqlite:///:memory:")

