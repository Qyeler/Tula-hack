import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    items = sqlalchemy.Column(sqlalchemy.String)
    items_cost = sqlalchemy.Column(sqlalchemy.String)

