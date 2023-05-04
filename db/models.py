from typing import List

from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.postges.postgres_base import Base


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_dora: Mapped[bool] = mapped_column(Boolean, default=True)
    # admin: Mapped["Admin"] = relationship("Admin", back_populates="user")


# class Admin(Base):
#     __tablename__ = "admins"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
#     message_id_choice: Mapped[int | None] = mapped_column(default=None)
#     user: Mapped["User"] = relationship("User", back_populates="admin")
#     dora_links: Mapped[List["Dora"]] = relationship("Dora", back_populates="admin")


class Dora(Base):
    __tablename__ = "dora"
    link: Mapped[str] = mapped_column(String(250), primary_key=True)
    file_id: Mapped[str | None] = mapped_column(String(150), default=None)
    # admin_id: Mapped[int | None] = mapped_column(ForeignKey("admins.id"), default=None)
    is_dataset: Mapped[bool | None] = mapped_column(Boolean, default=None)
    is_cool: Mapped[bool | None] = mapped_column(Boolean, default=None)
    # admin: Mapped["Admin"] = relationship("Admin", back_populates="dora_links")
