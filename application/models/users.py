from application import db

from .base import KeyedBase


class AnonymousUser:
    is_authenticated = False


class User(KeyedBase, db.AlchemyBase):
    __tablename__ = 'users'

    firebase_uid = db.Column(db.String(128), unique=True)

    @property
    def is_authenticated(self):
        return True
