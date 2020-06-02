# encoding=utf-8

from lib.api.okex.swap_api import SwapApi


class SwapBusiness:
    @classmethod
    def make_order_buy(cls, instrument_id, size, price, client_oid=''):
        """

        :param instrument_id:
        :param size:
        :param price:
        :param client_oid:
        :return:
        """
        pass

    @classmethod
    def revoke_order(cls, instrument_id, order_id='', client_oid=''):
        """

        :param instrument_id:
        :param order_id:
        :param client_oid:
        :return:
        """
        pass
