# encoding=utf-8

from lib.okex import spot_api
from lib.api.okex.base import ApiBase


class SpotApi(ApiBase):
    @classmethod
    def get_spot_api(cls):
        """
        获取现货 api实例
        :return:
        """
        if cls._spot_api is None:
            cls._spot_api = spot_api.SpotAPI(cls._api_key, cls._seceret_key, cls._passphrase, True)
        return cls._spot_api

    @classmethod
    def get_depth(cls, instrument_id):
        """
        公共-获取深度数据
        :param instrument_id:
        :return:
        """
        return cls.get_spot_api().get_depth(instrument_id)

    @classmethod
    def get_all_ticker(cls):
        """
        全部ticker信息
        :return:
        """
        return cls.get_spot_api().get_ticker()

    @classmethod
    def get_fills(cls, instrument_id, order_id, after='', before='', limit=''):
        """
        获取成交明细
        :param instrument_id:
        :param order_id:
        :param after:
        :param before:
        :param limit:
        :return:
        """
        return cls.get_spot_api().get_fills(instrument_id=instrument_id, order_id=order_id,
                                            after=after, before=before, limit=limit)

    @classmethod
    def get_trades(cls, instrument_id, limit=60):
        """
        公共-获取成交数据
        :param instrument_id:
        :param limit:
        :return:
        """
        return cls.get_spot_api().get_deal(instrument_id=instrument_id, after='', before='', limit=limit)

    @classmethod
    def get_specific_ticker(cls, instrument_id):
        """
        指定ticker信息
        :param instrument_id:
        :return:
        """
        return cls.get_spot_api().get_specific_ticker(instrument_id)

    @classmethod
    def get_kline(cls, instrument_id, start='', end='', granularity=60):
        """
        K线数据 (指定开始时间和结束时间区间，最多可以获取2000分钟前的数据)
        :param instrument_id:
        :param start:
        :param end:
        :param granularity:
        :return:
        """
        return cls.get_spot_api().get_kline(instrument_id=instrument_id, start=start, end=end, granularity=granularity)

    @classmethod
    def get_coin_info(cls, type="USDT"):
        """
        币对信息
        :param type:
        :return:
        """
        coin_info_list = cls.get_spot_api().get_coin_info()
        # 指定后缀
        if type and type in ['BTC', 'ETH', 'USDK', 'USDT', 'OKB']:
            result = []
            for coin_info in coin_info_list:
                ins_array = coin_info['instrument_id'].split('-')
                try:
                    if ins_array[1] == type:
                        result.append(coin_info)
                except IndexError:
                    continue
            return result
        return coin_info_list

