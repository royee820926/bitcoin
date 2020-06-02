# encoding=utf-8

import time
from lib.okex import swap_api
from lib.api.okex.base import ApiBase
from lib.common import TimeOperation


class SwapApi(ApiBase):
    @classmethod
    def get_instance(cls):
        """
        获取合约 api实例
        :return:
        """
        if cls._swap_api is None:
            cls._swap_api = swap_api.SwapAPI(cls.get_api_key(), cls.get_secret_key(), cls.get_passphrase(), True)
        return cls._swap_api

    @classmethod
    def get_position(cls):
        """
        获取账户所有合约的持仓信息。请求此接口，会在数据库遍历所有币对下的持仓数据，有大量的性能消耗,请求频率较低。建议用户传合约ID获取持仓信息。
        :return:
        """
        return cls.get_instance().get_position()

    @classmethod
    def get_one_position(cls, instrument_id):
        """
        获取某个合约的持仓信息
        :param instrument_id:
        :return:
        """
        return cls.get_instance().get_specific_position(instrument_id=instrument_id)

    @classmethod
    def get_accounts(cls):
        """
        获取所有币种合约的账户信息，当用户没有持仓时，保证金率为10000
        :return:
        """
        return cls.get_instance().get_accounts()

    @classmethod
    def get_one_account(cls, instrument_id):
        """
        获取单个币种合约的账户信息，当用户没有持仓时，保证金率为10000
        :param instrument_id:
        :return:
        """
        return cls.get_instance().get_coin_account(instrument_id=instrument_id)

    @classmethod
    def get_settings(cls, instrument_id):
        """
        获取某个合约的杠杆倍数，持仓模式
        :param instrument_id:
        :return:
        """
        return cls.get_instance().get_settings(instrument_id=instrument_id)

    @classmethod
    def set_leverage(cls, instrument_id, leverage, side):
        """
        设定某个合约的杠杆倍数
        :param instrument_id: 合约名称，如BTC-USD-SWAP,BTC-USDT-SWAP
        :param leverage: 杠杆倍数，填写1-100的数值
        :param side: 方向 1:逐仓-多仓；2:逐仓-空仓；3:全仓
        :return:
        """
        return cls.get_instance().set_leverage(instrument_id=instrument_id, leverage=leverage, side=side)

    @classmethod
    def take_order(cls, instrument_id, type, price, size, client_oid='', order_type='0', match_price=''):
        """
        下单
        :param instrument_id:
        :param type:
        :param price:
        :param size:
        :param client_oid:
        :param order_type:
        :param match_price:
        :return:
        """
        return cls.get_instance().take_order(instrument_id, type, price, size, client_oid=client_oid, order_type=order_type, match_price=match_price)

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
    def get_trade_fee(cls):
        """
        获取账户手续费费率
        :return:
        """
        return cls.get_instance().get_trade_fee()

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
        curr_ts = int(time.time())
        # 1天前
        start_ts = curr_ts - 24 * 60 * 60
        start_utc = start_ts - 8 * 60 * 60
        # 相隔200分钟（200条数据）
        end_utc = start_utc + 200 * 60

        while True:
            start_utcstr = time.strftime('%Y-%m-%dT%H:%M:00.000Z', time.localtime(start_utc))
            end_utcstr = time.strftime('%Y-%m-%dT%H:%M:00.000Z', time.localtime(end_utc))

            kline = cls.get_kline(instrument_id, start=start_utcstr, end=end_utcstr, granularity=granularity)
            if not bool(kline):
                break

            # 倒序添加
            for index in range(len(kline) - 1, -1, -1):
                # ISO8601 to string for +8:00
                time_8601 = kline[index][0]
                date_time = TimeOperation.string2datetime(time_8601, '%Y-%m-%dT%H:%M:00.000Z', hours=8)
                candle_begin_time = TimeOperation.datetime2string(date_time)

                result.append({
                    'candle_begin_time': candle_begin_time,
                    'open': float(kline[index][1]),
                    'high': float(kline[index][2]),
                    'low': float(kline[index][3]),
                    'close': float(kline[index][4]),
                    'volume': float(kline[index][5]),
                })
            # 更新时间
            start_utc = end_utc
            end_utc = start_utc + 200 * 60
            time.sleep(0.1)
        return result


