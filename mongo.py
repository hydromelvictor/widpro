#!/usr/bin/env python3
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()


class MongoConfig:
    """Manages MongoDB connection configuration."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoConfig, cls).__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

    def __init__(
            self,
            db: str,
            host: str = None,
            port: int = None,
            **kwargs: dict
    ):
        if not hasattr(self, 'initialized'):
            if not db:
                raise ValueError("Database name must be provided.")

            self.__host = host if host else '0.0.0.0'
            self.__port = int(port) if port else 27017

            try:
                self.__client = pymongo.MongoClient(
                    self.host, self.port, **kwargs
                )
                self.__db = self.__client[str(db)]
                self.initialized = True
            except pymongo.errors.ConnectionFailure as e:
                raise RuntimeError(f"Failed to connect to MongoDB: {e}")

    @property
    def db(self):
        """Access the database object."""
        return self.__db

    @property
    def host(self) -> str:
        """Get the host address for the MongoDB server."""
        return self.__host

    @host.setter
    def host(self, value: str) -> None:
        """Set the host address for the MongoDB server."""
        self.__host = value

    @property
    def port(self) -> int:
        """Get the port for the MongoDB server."""
        return self.__port

    @port.setter
    def port(self, value: int) -> None:
        """Set the port for the MongoDB server."""
        self.__port = value


# Initialize MongoConfig with environment variables
MongoConfig = MongoConfig(
    db=os.environ.get('MONGO_DB'),
    host=os.environ.get('MONGO_HOST'),
    port=os.environ.get('MONGO_PORT')
)
