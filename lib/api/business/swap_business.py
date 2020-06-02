# encoding=utf-8

from lib.api.okex.swap_api import SwapApi


class SwapBusiness:
    @classmethod
    def take_order_long(cls, instrument_id, size, price, client_oid=''):
        """

        :param instrument_id:
        :param size:
        :param price:
        :param client_oid:
        :return:
        """
        # 开多
        type = 1
        result = SwapApi.take_order(instrument_id=instrument_id, type=type, size=size, price=price, client_oid=client_oid,
                                    order_type='', match_price='')

    @classmethod
    def take_order_long_out(cls):
        # 平多
        type = 3


    @classmethod
    def take_order_short(cls):
        # 开空
        type = 2

    @classmethod
    def take_order_short_out(cls):
        # 平空
        type = 4

    @classmethod
    def revoke_order(cls, instrument_id, order_id='', client_oid=''):
        """

        :param instrument_id:
        :param order_id:
        :param client_oid:
        :return:
        """
        pass
