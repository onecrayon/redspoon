from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr

from application import db


class GlobalUuid(db.AlchemyBase):
    """Helper table for tracking global UUIDs across all models"""
    __tablename__ = 'global_uuids'

    uuid = db.Column(UUID(as_uuid=True), primary_key=True)
    # This is used to annotate global IDs to make by-hand lookups easier
    data_type = db.Column(db.String(64), nullable=True)


class KeyedBase:
    """Base mixin for including both primary ID and public-facing UUID columns
    
    This mixin should be used for all publicly-linkable models, as it provides both an
    auto-incrementing numeric ID for internal ForeignKeys, and a globally-unique UUID for:

    * Public ID usage (e.g. `/users/<uuid>` instead of `/users/<id>`)
    * Linking resources to multiple types (e.g. comments can potentially be attached to anything
      by linking through the global UUID table)
    """
    id = db.Column(db.Integer, primary_key=True)
    @declared_attr
    def uuid(cls):
        return db.Column(
            UUID(as_uuid=True),
            db.ForeignKey(GlobalUuid.uuid, ondelete='cascade'),
            unique=True
        )
