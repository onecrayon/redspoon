"""Database configuration and convenience access to common SQLAlchemy objects

Typical usage:
    from application import db
    class SomeModel(db.AlchemyBase):
        id = db.Column(db.Integer, primary_key=True)
"""
from sqlalchemy import (
    create_engine, Column, ForeignKey, BigInteger, Binary, Boolean, Date, DateTime, Enum, Float, Integer, Interval,
    LargeBinary, Numeric, PickleType, SmallInteger, String, Text, Time, Unicode, UnicodeText, alias, all_, and_, any_,
    asc, between, case, cast, collate, desc, distinct, except_, except_all, exists, extract, false, func, funcfilter,
    intersect, intersect_all, join, lateral, literal, literal_column, modifier, not_, null, nullsfirst, nullslast,
    or_, outerjoin, over, text, true, tuple_, type_coerce, union, union_all, within_group,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from .environment import settings

__all__ = (
    # Local variables
    'AlchemyBase',
    'SessionLocal',
    # SQLAlchemy convenience access
    #  "Holy verbosity, Batman! Why not programmatically include these like in Flask-SQLAlchemy?"
    #  "Well, Robin, I happen to like accurate autocomplete in my editors."
    # Schema shortcuts
    Column,
    ForeignKey,
    # Column type shortcuts
    BigInteger, Integer, SmallInteger,
    Binary, LargeBinary,
    Boolean,
    Date, DateTime, Time,
    Enum,
    Float,
    Interval,
    Numeric,
    PickleType,
    String, Text, Unicode, UnicodeText,
    # Relationships
    relationship,
    # SQL subset
    alias,
    all_, and_, any_, except_, except_all, not_, or_,
    asc, desc,
    between,
    case,
    cast,
    collate,
    distinct,
    exists,
    extract,
    false, true, null,
    func, funcfilter,
    intersect, intersect_all,
    join, outerjoin,
    lateral,
    literal, literal_column,
    modifier,
    nullsfirst, nullslast,
    over,
    text,
    tuple_,
    type_coerce,
    union, union_all,
    within_group,
)

# Setup base engine and session class
engine = create_engine(
    settings.db_url,
    echo=settings.debug
)
SessionLocal = sessionmaker(bind=engine)

# Setup our declarative base
AlchemyBase = declarative_base()
