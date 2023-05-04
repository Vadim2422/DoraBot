from environs import Env
from dataclasses import dataclass, field

from sqlalchemy import URL


@dataclass
class Bot:
    token: str
    admin: int

    def is_admin(self, user_id) -> bool:
        return user_id == self.admin


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
    postgres: Postgres
    vk_token: str


def load_config():
    env: Env = Env()
    env.read_env()

    return Config(bot=Bot(env('BOT_TOKEN'), admin=env.int('ADMIN')),
                  postgres=Postgres(drivername=env('P_DRIVERNAME'),
                                    host=env('P_HOST'),
                                    port=env('P_PORT'),
                                    username=env('P_USERNAME'),
                                    password=env('P_PASSWORD'),
                                    database=env('P_DATABASE'),
                                    query={}),
                  vk_token=env('VK_TOKEN'))


config = load_config()