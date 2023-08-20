from db import User
from db.repositories.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
