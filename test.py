# encoding=utf-8

from lib.api.okex.account_api import AccountApi
from lib.api.okex.spot_api import SpotApi
from lib.api.okex.index_api import IndexApi

# 资金账户API
# 账户信息
# result = AccountApi.get_wallet()

# result = AccountApi.get_currencies()
# result = AccountApi.get_coin_fee('btc')
# 资金划转
# 资金账户:6 -> 币币:1
# currency = 'USDT'
# amount = '10'
# account_from = '6'
# account_to = '1'
# result = AccountApi.coin_transfer(currency=currency, amount=amount, account_from=account_from, account_to=account_to,
#                                   sub_account='', instrument_id='', to_instrument_id='')

# 币币API
# 账户信息
# result = SpotApi.get_account_info()
# 指定币种的账户信息
result = SpotApi.get_coin_account_info('USDT')
print(result)
exit()
# 币对信息
# result = SpotApi.get_coin_info('USDT')
# 交易手续费费率
# result = SpotApi.get_trade_fee()
# 下单
instrument_id = 'EOS-USDT'
side = 'buy'
# 限价单
price = '39'
size = '1'
# result = SpotApi.take_order(instrument_id=instrument_id, side=side, price=price, size=size)

# 指数API
# 公共-获取指数成分
# result = IndexApi.get_index_constituents('BTC-USD')


# for item in result:
#     print(item)
print(result)
