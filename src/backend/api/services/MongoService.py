import pymongo as pm

from bson.json_util import dumps, loads

from sukasa.config import MONGO_CONNECTION


class MongoService:
    def __init__(self):
        self.mongo_connection = pm.MongoClient(
            host=MONGO_CONNECTION['host'],
            port=MONGO_CONNECTION['port'])

    def count_collection(self, collection_name):
        mongo_collection = self.mongo_connection[MONGO_CONNECTION['db']][collection_name]
        count = mongo_collection.count()
        return count

    def check_collection(self, collection_name):
        return collection_name in self.mongo_connection[MONGO_CONNECTION['db']].collection_names()

    def insert_to_collection(self, collection_name, data):
        mongo_collection = self.mongo_connection[MONGO_CONNECTION['db']][collection_name]
        data = dumps(data)
        mongo_collection.insert(loads(data))
        print("Successfully added data to the {} collection".format(collection_name))

    def get_from_collection(self, collection_name, mongo_id=None, property_id=None):
        mongo_collection = self.mongo_connection[MONGO_CONNECTION['db']][collection_name]
        if mongo_id is not None:
            return mongo_collection.find_one({'_id': mongo_id}, {'_id': 0})
        elif property_id is not None:
            return mongo_collection.find_one({'propertyId': property_id}, {'_id': 0})
        else:
            mongo_data = mongo_collection.find({}, {'_id': 0})
        return list(mongo_data)

    def search_collection(self, collection_name, search_string, status=None):
        mongo_collection = self.mongo_connection[MONGO_CONNECTION['db']][collection_name]
        search_dict = {'tags': search_string}
        if status:
            search_dict["$expr"] = {
                "$eq": [{ 
                    "$arrayElemAt": ["$status.status", -1] 
                    }, status]}
        search_results = mongo_collection.find(search_dict, {'_id': 0})
        return list(search_results)

    def find_user(self, collection_name, username):
        mongo_collection = self.mongo_connection[MONGO_CONNECTION['db']][collection_name]
        user_search_results = list(mongo_collection.find({'username': username}))
        for user in user_search_results:
            user['_id'] = str(user['_id'])
        return user_search_results

    def drop_database(self, collection_name=None):
        if collection_name is None:
            self.mongo_connection.drop_database(MONGO_CONNECTION['db'])
        else:
            self.mongo_connection[MONGO_CONNECTION['db']].drop_collection(collection_name)
