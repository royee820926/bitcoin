# encoding=utf-8

from lib.okex import spot_api
from lib.api.okex.base import ApiBase


class SpotApi(ApiBase):
    @classmethod
    def get_instance(cls):
        """
        获取现货 api实例
        :return:
        """
        if cls._spot_api is None:
            cls._spot_api = spot_api.SpotAPI(cls._api_key, cls._secret_key, cls._passphrase, True)
        return cls._spot_api

    @classmethod
    def get_account_info(cls):
        """
        币币账户信息
        :return:
        """
        return cls.get_instance().get_account_info()

    @classmethod
    def get_coin_account_info(cls, currency):
        """
        获取指定币种的账户信息
        :param currency:
        :return:
        """
        return cls.get_instance().get_coin_account_info(currency)

    @classmethod
    def get_coin_info(cls, type="USDT"):
        """
        币对信息
        :param type:
        :return:
        """
        return cls.get_instance().get_coin_info()

    @classmethod
    def take_order(cls, instrument_id, side, client_oid='', type='', size='', price='', order_type='0', notional=''):
        """
        下单
        :param instrument_id: 币对名称
        :param side: buy（买） 或 sell（卖）
        :param client_oid: 由您设置的订单ID来识别您的订单,格式是字母（区分大小写）+数字 或者 纯字母（区分大小写），1-32位字符 （不能重复）
        :param type: limit或market（默认是limit）。当以market（市价）下单，order_type只能选择0（普通委托）
        :param size: 买入或卖出的数量（限价单 | 市价单）
        :param price: 价格（限价单）
        :param order_type:
               0：普通委托（order type不填或填0都是普通委托）
               1：只做Maker（Post only）挂单
               2：全部成交或立即取消（FOK）
               3：立即成交并取消剩余（IOC）
        :param notional: 买入金额，市价买入时必填notional（市价单）
        :return:
        """
        return cls.get_instance().take_order(instrument_id=instrument_id, side=side, client_oid=client_oid, type=type,
                                             size=size, price=price, order_type=order_type, notional=notional)

    @classmethod
    def revoke_order(cls, instrument_id, order_id='', client_oid=''):
        """
        撤销指定订单
        :param instrument_id:
        :param order_id:
        :param client_oid:
        :return:
        """
        return cls.get_instance().revoke_order(instrument_id=instrument_id, order_id=order_id, client_oid=client_oid)

    @classmethod
    def get_order_list(cls, instrument_id, state, after='', before='', limit=''):
        """
        获取订单列表
        :param instrument_id:
        :param state:
        :param after:
        :param before:
        :param limit:
        :return:
        """
        return cls.get_instance().get_orders_list(instrument_id=instrument_id, state=state, after=after, before=before, limit=limit)

    @classmethod
    def get_orders_pending(cls, instrument_id, after='', before='', limit=''):
        """
        获取所有未成交订单
        :param instrument_id:
        :param after:
        :param before:
        :param limit:
        :return:
        """
        return cls.get_instance().get_orders_pending(instrument_id=instrument_id, after=after, before=before, limit=limit)

    @classmethod
    def get_trade_fee(cls):
        """
        获取当前账户交易手续费费率
        :return: taker: 吃单手续费率；maker: 挂单手续费率；timestamp: 数据返回时间
        """
        return cls.get_instance().get_trade_fee()

    @classmethod
    def get_depth(cls, instrument_id):
        """
        公共-获取深度数据
        :param instrument_id:
        :return:
        """
        return cls.get_instance().get_depth(instrument_id)

    @classmethod
    def get_all_ticker(cls):
        """
        全部ticker信息
        :return:
        """
        return cls.get_instance().get_ticker()

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
        return cls.get_instance().get_fills(instrument_id=instrument_id, order_id=order_id,
                                            after=after, before=before, limit=limit)

    @classmethod
    def get_trades(cls, instrument_id, limit=60):
        """
        公共-获取成交数据
        :param instrument_id:
        :param limit:
        :return:
        """
        return cls.get_instance().get_deal(instrument_id=instrument_id, limit=limit)

    @classmethod
    def get_specific_ticker(cls, instrument_id):
        """
        指定ticker信息
        :param instrument_id:
        :return:
        """
        return cls.get_instance().get_specific_ticker(instrument_id)

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
        return cls.get_instance().get_kline(instrument_id=instrument_id, start=start, end=end, granularity=granularity)

