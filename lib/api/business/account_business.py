# encoding=utf-8
# 账户操作

from lib.api.okex.account_api import AccountApi
from lib.okex.exceptions import OkexAPIException


class AccountBusiness:
    @classmethod
    def coin_transfer_from_spot_to_margin(cls, amount, to_instrument_id):
        """
        资金划转: 现货划转资金到杠杆账户
        account_from: 1、币币；3、交割合约；4、法币账户；5、币币杠杆；6、资金账户
                      8、余币宝；9、永续合约账户；12、期权合约；14、挖矿账户；17、借贷账户
        :param amount: 划转金额 单位：USDT
        :param to_instrument_id: 转入杠杆币对，例如：EOS-USDT
        :return: {'result': True, 'amount': '1.00000000', 'from': '1', 'currency': 'USDT', 'transfer_id': '186889369', 'to': '5'}
        """
        currency = 'USDT'
        account_from = 1
        account_to = 5
        try:
            result = AccountApi.coin_transfer(currency=currency, amount=amount, account_from=account_from,
                                              account_to=account_to, to_instrument_id=to_instrument_id)
        except OkexAPIException:
            # 金额不足
            return False
        return result

    @classmethod
    def coin_transfer_from_margin_to_spot(cls, amount, to_instrument_id):
        """
        资金划转：杠杆账户划转资金到现货账户
        :param amount: 划转金额 单位：USDT
        :param to_instrument_id: 杠杆转出币对，例如：EOS-USDT
        :return:
        """
        currency = 'USDT'
        account_from = 5
        account_to = 1
        try:
            result = AccountApi.coin_transfer(currency=currency, amount=amount, account_from=account_from,
                                              account_to=account_to, instrument_id=to_instrument_id)
        except OkexAPIException:
            # 金额不足
            return False
        return result

    @classmethod
    def coin_transfer_from_spot_to_swap(cls, amount, to_instrument_id):
        """
        资金划转：现货账户划转资金到永续合约账户
        :param amount:
        :param to_instrument_id:
        :return:
        """
        currency = 'USDT'
        account_from = 1
        account_to = 9
        try:
            result = AccountApi.coin_transfer(currency=currency, amount=amount, account_from=account_from,
                                              account_to=account_to, to_instrument_id=to_instrument_id)
        except OkexAPIException:
            # 金额不足
            return False
        return result

    @classmethod
    def coin_transfer_from_swap_to_spot(cls, amount, to_instrument_id):
        """
        资金划转：永续合约账户划转资金到现货账户
        :param amount:
        :param to_instrument_id:
        :return:
        """
        currency = 'USDT'
        account_from = 9
        account_to = 1
        try:
            result = AccountApi.coin_transfer(currency=currency, amount=amount, account_from=account_from,
                                              account_to=account_to, instrument_id=to_instrument_id)
        except OkexAPIException:
            # 金额不足
            return False
        return result


