from threading import Lock
import pymongo

from tournament.logger import Logger
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
            return self.connections[str(service_name)]
        except KeyError:
            with self.create_lock:
                try:
                    return self.connections[str(service_name)]
                except KeyError:
                    return self._create_connection(service_name)

    def _create_connection(self, service_name):
        conn = ""
        if service_name == Services.DATABASE:
            # Not at all advisable to use authenticate details like this
            Logger().info('connection_creation', action='started', service=str(service_name),
                          conn_config=ConnectionConfigProvider().get_connection(service_name))
            conn = pymongo.MongoClient(ConnectionConfigProvider().get_connection(service_name))
            Logger().info('connection_creation', action='finished', conn=conn)
        elif service_name == Services.MESSAGE_BROKER:
            conn = ""

        Logger().info('connection_creation', action='setting_connection_info', service_name=service_name,
                      conn=conn)
        self.connections[str(service_name)] = conn
        return conn
