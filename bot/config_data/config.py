from dataclasses import dataclass, field
from dotenv import load_dotenv
from sqlalchemy import URL
import os


@dataclass
class Bot:
    token: str
    admin: int

    def is_admin(self, user_id) -> bool:
        return user_id == self.admin


@dataclass
class Vk:
    user_token: str
    group_token: str
    api_v: str


@dataclass
class Postgres:
    drivername: str
    host: str
    port: str
    username: str
    password: str
    database: str
    query: dict

    def get_url(self):
        return URL(**self.__dict__)


@dataclass
class Config:
    bot: Bot
    secret: str
    vk: Vk


def load_config():
    load_dotenv()

    return Config(bot=Bot(os.getenv('BOT_TOKEN'), admin=int(os.getenv('ADMIN'))),
                  secret=os.getenv('SECRET'),
                  vk=Vk(user_token=os.getenv('USER_TOKEN'),
                        group_token=os.getenv('GROUP_TOKEN'),
                        api_v=os.getenv('API_V'))
                  )
    # postgres=Postgres(drivername=os.getenv('POSTGRES_DRIVERNAME'),
    #                   host=os.getenv('POSTGRES_HOST'),
    #                   port=os.getenv('POSTGRES_PORT'),
    #                   username=os.getenv('POSTGRES_USER'),
    #                   password=os.getenv('POSTGRES_PASSWORD'),
    #                   database=os.getenv('POSTGRES_DB'),
    #                   query={}),


config = load_config()
