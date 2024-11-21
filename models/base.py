"""Declaration of base class for all models"""

from sqlalchemy.orm import DeclarativeBase, declarative_base

__all__ = (
    "Base",
)

Base: DeclarativeBase = declarative_base()
