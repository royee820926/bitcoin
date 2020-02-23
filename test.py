# encoding=utf-8

from test.test_api import TestApi

# 资金账户API
# 账户信息
# result = TestApi.account_get_wallet()

# result = TestApi.account_get_currencies()
# result = TestApi.account_get_coin_fee('btc')
# 资金划转
# 资金账户:6 -> 币币:1
currency = 'USDT'
amount = '10'
account_from = '6'
account_to = '1'
result = TestApi.account_coin_transfer(currency=currency, amount=amount, account_from=account_from, account_to=account_to,
                                       sub_account='', instrument_id='', to_instrument_id='')

# 币币API
# 账户信息
# result = TestApi.spot_get_account_info()
# 指定币种的账户信息
# result = TestApi.spot_get_coin_account_info('LTC')
# 币对信息
# result = TestApi.spot_get_coin_info('USDT')

# 指数API
# 公共-获取指数成分
# result = TestApi.index_get_index_constituents('BTC-USD')


# for item in result:
#     print(item)
print(result)
