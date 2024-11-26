from sqlalchemy.orm import DeclarativeBase

from .. import db


class Base(DeclarativeBase):
    __abstract__ = True