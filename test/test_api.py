# encoding=utf-8

from lib.api.okex.account_api import AccountApi
from lib.api.okex.spot_api import SpotApi
from lib.api.okex.index_api import IndexApi


class TestApi:
    ################# spot #################
    @classmethod
    def spot_get_kline(cls, coin_name):
        return SpotApi.get_kline(coin_name)

    @classmethod
    def spot_get_account_info(cls):
        return SpotApi.get_account_info()

    @classmethod
    def spot_get_coin_account_info(cls, currency):
        return SpotApi.get_coin_account_info(currency)

    @classmethod
    def spot_get_coin_info(cls, type):
        return SpotApi.get_coin_info(type)


    ################# account #################
    @classmethod
    def account_get_wallet(cls):
        return AccountApi.get_wallet()

    @classmethod
    def account_get_currencies(cls):
        return AccountApi.get_currencies()

    @classmethod
    def account_get_coin_fee(cls, currency):
        return AccountApi.get_coin_fee(currency)

    @classmethod
    def account_coin_transfer(cls, currency, amount, account_from, account_to, sub_account='', instrument_id='', to_instrument_id=''):
        return AccountApi.coin_transfer(currency=currency, amount=amount, account_from=account_from, account_to=account_to,
                                        sub_account=sub_account, instrument_id=instrument_id, to_instrument_id=to_instrument_id)

    ################# index #################
    @classmethod
    def index_get_index_constituents(cls, instrument_id):
        return IndexApi.get_index_constituents(instrument_id)
