from db.models import Admin
from db.repositories.repository import SQLAlchemyRepository


class AdminRepository(SQLAlchemyRepository):
    model = Admin
