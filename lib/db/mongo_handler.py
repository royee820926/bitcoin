# encoding=utf-8

from pymongo import MongoClient
from config.mongo import mongo_host, mongo_port


def get_mongo_handler():
    host = mongo_host
    port = mongo_port
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
        if cls._client is None:
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

    @classmethod
    def get_spot_kline(cls, instrument_id, start=0, end=0):
        """
        获取现货mongodb的K线数据
        :param instrument_id
        :param start:
        :param end:
        :return:
        """
        if start == 0 and end == 0:
            return []
        collection = cls.get_spot_collection(instrument_id)
        condition = {
            'time': {}
        }

        if start != 0:
            condition['time']['$gte'] = start
        if end != 0:
            condition['time']['$lt'] = end
        result = collection.find(condition)
        return result

    @classmethod
    def get_swap_kline(cls, instrument_id, start=0, end=0):
        """
        获取合约mongodb的K线数据
        :param instrument_id
        :param start:
        :param end:
        :return:
        """
        collection = cls.get_swap_collection(instrument_id)
        result = collection.find({"time": {"$gte": int(start), "$lt": int(end)}})
        return result
