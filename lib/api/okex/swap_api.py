# encoding=utf-8

from lib.okex import swap_api
from lib.api.okex.base import ApiBase


class SwapApi(ApiBase):
    @classmethod
    def get_swap_api(cls):
        """
        获取合约 api实例
        :return:
        """
        if cls._swap_api is None:
            cls._swap_api = swap_api.SwapAPI(cls._api_key, cls._seceret_key, cls._passphrase, True)
        return cls._swap_api

    @classmethod
    def get_trades(cls, instrument_id, after='', before='', limit=''):
        """
        公共-获取成交数据
        :param instrument_id:
        :param after:
        :param before:
        :param limit:
        :return:
        """
        return cls.get_swap_api().get_trades(instrument_id=instrument_id, after=after, before=before, limit=limit)

    @classmethod
    def get_kline(cls, instrument_id, start='', end='', granularity=60):
        """
        获取合约的K线数据。k线数据最多可获取最近1440条。
        :param instrument_id:
        :param start:
        :param end:
        :param granularity:
        :return:
        """
        return cls.get_swap_api().get_kline(instrument_id=instrument_id, start=start, end=end, granularity=granularity)
