from threading import local

from models.settings import Settings
from models.database import DataBase


class Shared(local):
    settings: Settings
    database: DataBase


shared = Shared()
