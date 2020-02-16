# encoding=utf-8

from pymongo import MongoClient


def get_mongo_handler():
    host = '192.168.2.110'
    # host = '192.168.10.10'
    port = '27017'
    db_name = 'test_db'

    uri = 'mongodb://{host}:{port}/{db_name}?authSource={auth_source}' \
        .format(host=host, port=port, db_name=db_name, auth_source=db_name)
    client = MongoClient(uri)
    return client


def get_spot_collection(collection_name):
    """
    获取现货数据集合
    :param collection_name:
    :return:
    """
    client = get_mongo_handler()
    database = client['okex_spot']
    collection = database[collection_name]
    return collection


def get_swap_collection(collection_name):
    """
    获取合约数据集合
    :param collection_name:
    :return:
    """
    client = get_mongo_handler()
    database = client['okex_swap']
    collection = database[collection_name]
    return collection


class MongoHandle:
    _client = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._client = get_mongo_handler()
        return cls._client

    @classmethod
    def get_spot_collection(cls, collection_name):
        """
        获取现货数据库的连接
        :param collection_name:
        :return:
        """
        client = cls.get_instance()
        database = client['okex_spot']
        return database[collection_name]

    @classmethod
    def get_swap_collection(cls, collection_name):
        """
        获取合约数据库的连接
        :param collection_name:
        :return:
        """
        client = cls.get_instance()
        database = client['okex_swap']
        return database[collection_name]
