# encoding=utf-8

from lib.db.mongo_handler import get_spot_collection
from lib.api.okex.spot_api import SpotApi
import pandas as pd
import time

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 500)
pd.set_option('display.min_rows', 500)

instrument_id = 'BTC-USDT'
collection = get_spot_collection(instrument_id)

# 取出多少条1分钟K线
kline_length = 60 * 24
temp = collection.find().sort([('time', -1)]).limit(kline_length)
result = []
for item in temp:
    result.append({
        'time'      : item['time'],
        'open'      : item['open'],
        'high'      : item['high'],
        'low'       : item['low'],
        'close'     : item['close'],
        'volume'    : item['volume'],
    })
# 最后一条时间戳（请求kline接口时，换算成UTC时间）
last_stamp_zh = result[0]['time'] - 8 * 3600
result = reversed(result)
for item in result:
    print(item)
# 转换ISO8601
# 加60秒掠过last_stamp
last_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.localtime(last_stamp_zh + 60))
now_kline = SpotApi.get_kline(instrument_id, start=last_time)

print(last_stamp_zh)
print(last_time)
for item in now_kline:
    print(item)

exit()

# exit()
# print(result)
