# encoding=utf-8
# 现货交易

from lib.api.okex.spot_api import SpotApi


class SpotBusiness:
    @classmethod
    def make_order_buy(cls, instrument_id, size, price, client_oid=''):
        """
        限价单-下单买入
        :param instrument_id:
        :param size: 买入或卖出的数量
        :param price: 单价
        :param client_oid:
        :return:
        """
        side = 'buy'
        result = SpotApi.take_order(instrument_id=instrument_id, side=side, price=price, size=size, client_oid=client_oid)
        return result

    @classmethod
    def take_order_buy(cls, instrument_id, notional, size='', client_oid=''):
        """
        市价单-下单买入（也可以用限价单代替）
        :param instrument_id:
        :param size: 市价卖出数量
        :param notional: 买入金额
        :param client_oid:
        :return:
        """
        side = 'buy'
        result = SpotApi.take_order(instrument_id=instrument_id, side=side, notional=notional, size=size, client_oid=client_oid)
        return result

    @classmethod
    def revoke_order(cls, instrument_id, order_id='', client_oid=''):
        """
        撤销下单
        :param instrument_id:
        :param order_id:
        :param client_oid:
        :return:
        """
        result = SpotApi.revoke_order(instrument_id=instrument_id, order_id=order_id, client_oid=client_oid)
        return result

    @classmethod
    def make_order_sell(cls, instrument_id, size, price, client_oid=''):
        """
        限价单-下单卖出
        :return:
        """
        # 获取扣除手续费
        trade_fee = SpotApi.get_trade_fee()
        taker_rate = float(trade_fee['taker'])
        size = size * (1 - taker_rate)

        side = 'sell'
        result = SpotApi.take_order(instrument_id=instrument_id, side=side, price=price, size=size,
                                    client_oid=client_oid)
        return result

