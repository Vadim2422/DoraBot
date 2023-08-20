from db import Links
from db.repositories.repository import SQLAlchemyRepository


class LinksRepository(SQLAlchemyRepository):
    model = Links
