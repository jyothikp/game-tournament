from threading import Lock
import pymongo
from tournament.models import Services
from tournament.provider import ConnectionConfigProvider
from tournament.utils import Singleton


class ConnectionPool:
    __metaclass__ = Singleton

    def __init__(self):
        self.connections = {}
        self.create_lock = Lock()

    def get_connection(self, service_name):
        try:
            return self.connections[service_name]
        except KeyError:
            with self.create_lock:
                try:
                    return self.connections[service_name]
                except KeyError:
                    return self._create_connection(service_name)

    def _create_connection(self, service_name):
        conn = ""
        if service_name == Services.DATABASE:
            conn = pymongo.MongoClient(ConnectionConfigProvider().get_connection(service_name))
        elif service_name == Services.MESSAGE_BROKER:
            conn = ""
        self.connections[str(service_name)] = conn
        return conn
