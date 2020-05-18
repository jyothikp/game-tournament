import json

import pkg_resources

from tournament.utils import Singleton


class ConnectionConfigProvider(object):
    __metaclass__ = Singleton
    data_file = 'config.json'

    def __init__(self):
        self.data = self.read_config(__name__, self.data_file)['connection']

    @classmethod
    def read_config(cls, module, path):
        data = pkg_resources.resource_string(module, path)
        return json.loads(data)

    def get_connection(self, service_name):
        return self.data.get(str(service_name))
