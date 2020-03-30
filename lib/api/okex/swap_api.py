# encoding=utf-8

import time
from lib.okex import swap_api
from lib.api.okex.base import ApiBase
from lib.common import TimeOption


class SwapApi(ApiBase):
    @classmethod
    def get_instance(cls):
        """
        获取合约 api实例
        :return:
        """
        if cls._swap_api is None:
            cls._swap_api = swap_api.SwapAPI(cls._api_key, cls._secret_key, cls._passphrase, True)
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
        return cls.get_instance().get_trades(instrument_id=instrument_id, after=after, before=before, limit=limit)

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
        return cls.get_instance().get_kline(instrument_id=instrument_id, start=start, end=end, granularity=granularity)

    @classmethod
    def get_kline_more(cls, instrument_id, granularity=60):
        """
        指定开始和结束时间，获取更多的K线记录
        :param instrument_id:
        :param granularity:
        :return:
        """
        result = []
        # '%Y-%m-%dT%H:%M:00.000Z'
        start_time = '2020-03-30T09:00:00.000Z'
        end_time = '2020-03-30T09:30:00.000Z'
        # start_stamp = time.strftime('%Y-%m-%dT%H:%M:00.000Z', time.localtime(time.time()))
        # print(type(start_stamp))
        # print(type(start_time))
        # print(instrument_id)
        # exit()
        kline = cls.get_kline(instrument_id, end=end_time)
        for item in kline:
            print(item)
        exit()

        for index in range(len(kline) - 1, -1, -1):
            candle_begin_time = kline[index][0]

            format_str = '%Y-%m-%dT%H:%M:%S.%fZ'
            date_time = TimeOption.string2datetime(candle_begin_time, format_str, hours=8)
            time_str = TimeOption.datetime2string(date_time)

            kline[index][0] = time_str
            result.append(kline[index])

        for item in result:
            print(item)
        exit()


