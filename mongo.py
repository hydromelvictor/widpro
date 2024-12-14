#!/usr/bin/env python3
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()


class MongoConfig:
    def __init__(self, db, host=None, port=None, **kwargs):
        self.__host = host if host else '0.0.0.0'
        self.__port = port if port else 27017
        self.__client = pymongo.MongoClient(self.host, self.port, **kwargs)
        self.__db = self.__client[str(db if db else 'test')]

    @property
    def db(self) -> pymongo.database.Database:
        return self.__db

    @property
    def host(self) -> str:
        return self.__host

    @host.setter
    def host(self, value) -> None:
        self.__host = value

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, value) -> None:
        self.__port = value


MongoConfig = MongoConfig(
    db=os.environ.get('MONGO_DB'),
    host=os.environ.get('MONGO_HOST'),
    port=os.environ.get('MONGO_PORT')
)
