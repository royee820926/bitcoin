# encoding=utf-8

from lib.api.okex.base import ApiBase
from lib.okex import account_api


class AccountApi(ApiBase):
    @classmethod
    def get_instance(cls):
        """
        获取资金账户 api实例
        :return:
        """
        if cls._account_api is None:
            cls._account_api = account_api.AccountAPI(cls._api_key, cls._secret_key, cls._passphrase, True)
        return cls._account_api

    @classmethod
    def get_wallet(cls):
        """
        资金账户信息
        :return:
        """
        return cls.get_instance().get_wallet()

    @classmethod
    def coin_transfer(cls, currency, amount, account_from, account_to, sub_account='', instrument_id='', to_instrument_id=''):
        """
        资金划转
        account_from 转出账户
                     0:子账户，1:币币，3:合约，4:C2C，5:币币杠杆，6:资金账户，8:余币宝，9:永续合约，12:期权
        sub_account  子账号登录名，from或to指定为0时，sub_account为必填项
        instrument_id
                     杠杆转出币对 或者 usdt保证金合约转出的underlying，如：btc-usdt，仅限已开通杠杆币对或者合约的underlying。
        to_instrument_id
                     杠杆转入币对 或者 usdt保证金合约转入的underlying，如：btc-usdt，仅限已开通杠杆币对或者合约的underlying。
        :return:
        """
        return cls.get_instance().coin_transfer(currency=currency, amount=amount, account_from=account_from, account_to=account_to,
                                                sub_account=sub_account, instrument_id=instrument_id, to_instrument_id=to_instrument_id)

    @classmethod
    def get_asset_valuation(cls):
        """
        获取账户资产估值
        :return:
        """
        pass
        # return cls.get_instance().get_asset_valuation()

    @classmethod
    def get_currencies(cls):
        """
        获取币种列表
        :return:
        """
        return cls.get_instance().get_currencies()

    @classmethod
    def get_coin_fee(cls, currency):
        """
        提币手续费
        :param currency: 如 btc
        :return:
        """
        return cls.get_instance().get_coin_fee(currency=currency)
