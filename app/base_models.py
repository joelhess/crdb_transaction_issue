from datetime import datetime

from sqlalchemy import DateTime, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseSQLModel(DeclarativeBase):
    pass


class BaseTimestampModel:
    """Adds `created` and `modified` columns to a derived declarative model.

    The `created` column is handled through a default and the `modified`
    column is handled through a `before_update` event that propagates
    for all derived declarative models.
    Derived From: https://sqlalchemy-utils.readthedocs.io/en/latest/_modules/sqlalchemy_utils/models.html#Timestamp
    changed to use "modified" instead of "updated"
    """

    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    modified: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)


@event.listens_for(BaseTimestampModel, "before_update", propagate=True)
def timestamp_before_update(mapper, connection, target) -> None:  # type: ignore
    # When a model with a timestamp is updated; force update the updated timestamp.
    target.modified = datetime.utcnow()
