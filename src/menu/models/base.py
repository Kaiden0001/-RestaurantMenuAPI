import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
        server_default=str(uuid.uuid4())
    )
