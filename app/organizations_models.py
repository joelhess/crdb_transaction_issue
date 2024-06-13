"""Provides the Organization model."""

from typing import Annotated, Optional
from uuid import UUID

from sqlalchemy import UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base_models import BaseSQLModel, BaseTimestampModel

UNIQUE_ORG_NAME = "unique__org_name"


class Organization(BaseSQLModel, BaseTimestampModel):
    """Organization table model."""

    __tablename__ = "organization"
    id: Mapped[
        Annotated[
            UUID,
            mapped_column(
                primary_key=True, index=True, server_default=text("gen_random_uuid()")
            ),
        ]
    ]
    revision: Mapped[Annotated[int, mapped_column(default=0)]]

    # organization_memberships: Mapped[list["OrganizationMembership"]] = relationship(  # type: ignore # noqa: F821(
    #     back_populates="organization", lazy="selectin"
    # )

    # tenants: Mapped[list["Tenant"]] = relationship(back_populates="organization", lazy="selectin")  # type: ignore # noqa: F821
    name: Mapped[
        Annotated[
            str,
            mapped_column(unique=True),
        ]
    ]
    label: Mapped[str | None]
    is_admin: Mapped[
        Annotated[
            Optional[bool],
            mapped_column(default=None, unique=True),
        ]
    ]

    __table_args__ = (UniqueConstraint("name", name=UNIQUE_ORG_NAME),)
