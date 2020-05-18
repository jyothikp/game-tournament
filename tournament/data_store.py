from bson import ObjectId
from pymongo import ReturnDocument

from tournament.connection_pool import ConnectionPool
from tournament.models import Services


class DataStore:
    DB_NAME = 'game'

    def __init__(self, collection):
        self.conn = self.__get_connection()
        self.collection = collection
        self.cursor = self.__get_db()[collection]

    def _create_indexes(self, indexes):
        self.cursor.create_indexes(indexes)

    @classmethod
    def __get_connection(cls):
        return ConnectionPool().get_connection(Services.DATABASE)

    def __get_db(self):
        return self.conn[self.DB_NAME]

    def save(self, model):
        return self.cursor.save(model.to_dict())

    def update_one(self, query, data):
        return self.cursor.find_one_and_update(query, {'$set': data}, upsert=True,
                                               return_document=ReturnDocument.AFTER)['_id']

    def find_by_id(self, obj_id):
        return self.cursor.find_one({'_id': ObjectId(obj_id)})

    def find(self, query):
        return self.cursor.find(query)

    def find_one(self, query):
        return self.cursor.find_one(query)
