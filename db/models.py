from datetime import datetime
from sqlalchemy import Integer, Boolean, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_dora: Mapped[bool] = mapped_column(Boolean, default=True)
    data = mapped_column(DateTime, default=datetime.now)
    # admin: Mapped["Admin"] = relationship("Admin", back_populates="user")


class Admin(Base):
    __tablename__ = "admins"
    user_id = mapped_column(Integer, primary_key=True)
    selection_msg_id = mapped_column(Integer)
    file_id = mapped_column(String(250))


# class Admin(Base):
#     __tablename__ = "admins"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
#     message_id_choice: Mapped[int | None] = mapped_column(default=None)
#     user: Mapped["User"] = relationship("User", back_populates="admin")
#     dora_links: Mapped[List["Dora"]] = relationship("Dora", back_populates="admin")


class Links(Base):
    __tablename__ = "links"
    link = mapped_column(String(250), primary_key=True)
    file_id = mapped_column(String(150), default=None)
    date = mapped_column(DateTime)
    date_create = mapped_column(DateTime, default=datetime.now)
    # admin_id: Mapped[int | None] = mapped_column(ForeignKey("admins.id"), default=None)
    is_dataset = mapped_column(Boolean, default=None)
    is_cool = mapped_column(Boolean, default=None)
    admin_id = mapped_column(ForeignKey("admins.user_id"))
    # admin: Mapped["Admin"] = relationship("Admin", back_populates="dora_links")
