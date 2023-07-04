from ZODB import DB
from persistent.dict import PersistentDict
from trackseriessaver.config import database_path
import os


class SingletonZODB:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        # check if data folder exists, otherwise create it
        if not os.path.exists(database_path):
            os.mkdir(database_path)
        self.db = DB(os.path.join(database_path, "data.fs"))
        self.conn = self.db.open()
        self.dbroot = self.conn.root()

        if "app_data" not in self.dbroot:
            print("Initializing database...")
            # init the database
            self.dbroot["app_data"] = PersistentDict()


zodb = SingletonZODB.instance()