# encoding=utf-8

from lib.okex import index_api
from lib.api.okex.base import ApiBase


class IndexApi(ApiBase):
    @classmethod
    def get_instance(cls):
        """
        获取现货 api实例
        :return:
        """
        if cls._index_api is None:
            cls._index_api = index_api.IndexAPI(cls.get_api_key(), cls.get_secret_key(), cls.get_passphrase(), True)
        return cls._index_api

    @classmethod
    def get_index_constituents(cls, instrument_id):
        """
        获取指数成分。此接口为公共接口，不需要身份验证。
        指数币对（如BTC-USD）
        :param instrument_id:
        :return:
        """
        return cls.get_instance().get_index_constituents(instrument_id)
