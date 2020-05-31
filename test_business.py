# encoding=utf-8

from lib.api.okex.account_api import AccountApi
from lib.api.okex.spot_api import SpotApi
from lib.api.okex.swap_api import SwapApi

from lib.api.business.account_business import AccountBusiness

# business 资金划转
# result = AccountBusiness.coin_transfer_from_sport_to_margin(1, 'EOS-USDT')
result = AccountBusiness.coin_transfer_from_margin_to_spot(1, 'EOS-USDT')
print(result)
print('hhhh')
exit()


# 账户接口
# 资金账户信息
# result = AccountApi.get_wallet()
# result = AccountApi.get_currency('LTC')
# 币种列表
# result = AccountApi.get_currencies()
# 资金划转
# result = AccountApi.coin_transfer(currency, amount, account_from, account_to, sub_account='', instrument_id='', to_instrument_id='')
# result = AccountApi.coin_transfer('USDT', 1, )


# 币币接口
result = SpotApi.get_account_info()
# result = SpotApi.get_coin_account_info('LTC')
# result = SpotApi.get_coin_info()
# result = SpotApi.get_kline('BTC-USDT')

# 合约接口
# result = SwapApi.get_accounts()


# print(result)
for item in result:
    print(item)
