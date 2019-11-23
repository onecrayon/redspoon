from application import db

from .base import KeyedBase


class User(KeyedBase, db.AlchemyBase):
    __tablename__ = 'users'

    email = db.Column(db.String(256), unique=True)
