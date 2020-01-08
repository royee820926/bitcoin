# encoding=utf-8

from lib.api.okex.spot_api import SpotApi
from lib.api.okex.swap_api import SwapApi
from config.spot_coin import spot_coin_type
from lib.db.mongo_handler import get_spot_collection
from lib.okex.exceptions import OkexAPIException
import time
import threading
import requests

# 现货
# # result = SpotApi.get_kline('BTC-USDT')
# result = SpotApi.get_kline(instrument_id='BTC-USDT', start='2020-01-03T15:03:00.000Z', end='2020-01-03T15:07:00.000Z')
#
# for item in result:
#     print(item)

# 合约
# result = SwapApi.get_kline('BTC-USD-SWAP')
# print(result)
# print(len(result))


# print(int(time.time()))
# result = 1578158115
#
# result = time.strftime('%Y-%m-%d %H:%M:00', time.localtime(result))
# print(result)



