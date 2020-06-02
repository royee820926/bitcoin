# encoding=utf-8

from lib.api.business.account_business import AccountBusiness
from lib.api.business.spot_business import SpotBusiness
from lib.api.business.swap_business import SwapBusiness

# business 资金划转
# result = AccountBusiness.coin_transfer_from_spot_to_margin(1, to_instrument_id='EOS-USDT')
# result = AccountBusiness.coin_transfer_from_margin_to_spot(1, to_instrument_id='EOS-USDT')
# result = AccountBusiness.coin_transfer_from_spot_to_swap(1, to_instrument_id='EOS-USDT')
# result = AccountBusiness.coin_transfer_from_swap_to_spot(1, to_instrument_id='EOS-USDT')

# 现货
# 限价单下单买入
# result = SpotBusiness.make_order_buy(instrument_id='EOS-USDT', size=1, price=3)
# 现价单撤销
# result = SpotBusiness.revoke_order(instrument_id='EOS-USDT', order_id='5002699322376192')
# 限价单卖出
# result = SpotBusiness.make_order_sell(instrument_id='EOS-USDT', size=1, price=2.8)

# 永续合约
# 下单
# result = SwapBusiness
#
# print(result)
# exit()

#############################################################################
from lib.api.okex.account_api import AccountApi
from lib.api.okex.spot_api import SpotApi
from lib.api.okex.swap_api import SwapApi

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
# result = SpotApi.get_account_info()
# result = SpotApi.get_coin_account_info('LTC')
# 获取币对信息
# result = SpotApi.get_coin_info()
# 获取指定币对信息
# result = SpotApi.get_one_coin_info('EOS-USDT')
# result = SpotApi.get_all_ticker()
# result = SpotApi.get_one_ticker('EOS-USDT')
# result = SpotApi.get_kline('BTC-USDT')

# 合约接口
# 获取所有币种合约的账户信息，当用户没有持仓时，保证金率为10000
# result = SwapApi.get_accounts()
# 获取账户手续费费率
# result = SwapApi.get_trade_fee()


print(result)
# for item in result:
#     print(item)
