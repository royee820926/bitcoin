# encoding=utf-8

from lib.db.mongo_handler import get_spot_collection
from lib.api.okex.spot_api import SpotApi
import pandas as pd
import time

pd.set_option('expand_frame_repr', False)
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.min_rows', 500)
pd.set_option('display.max_rows', None)

instrument_id = 'BTC-USDT'
collection = get_spot_collection(instrument_id)

# 取出多少条1分钟K线
kline_length = 60 * 24
# 从数据库读取K线记录
temp = collection.find().sort([('time', -1)]).limit(kline_length)
result = []
last_stamp_zh = 0
for item in temp:
    if last_stamp_zh == 0:
        # 最后一条时间戳（请求kline接口时，换算成UTC时间）
        last_stamp_zh = int(item['time']) - 8 * 3600
    result.append({
        'candle_begin_time' : time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['time'])),
        'open'              : float(item['open']),
        'high'              : float(item['high']),
        'low'               : float(item['low']),
        'close'             : float(item['close']),
        'volume'            : float(item['volume']),
    })

result = list(reversed(result))

# 转换ISO8601
# 加60秒掠过last_stamp
last_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.localtime(last_stamp_zh + 60))
# 从接口补全K线记录
temp = SpotApi.get_kline(instrument_id, start=last_time)
add_kline = []
for item in temp:
    time_array = time.strptime(item[0], "%Y-%m-%dT%H:%M:%S.000Z")
    timestamp = time.mktime(time_array) + 8 * 3600
    candle_begin_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

    result.append({
        'candle_begin_time' : candle_begin_time,
        'open'              : float(item[1]),
        'high'              : float(item[2]),
        'low'               : float(item[3]),
        'close'             : float(item[4]),
        'volume'            : float(item[5]),
    })

df = pd.DataFrame(result)
df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'], format='%Y-%m-%d %H:%M:%S')
# print(type(df.iloc[0]['candle_begin_time']))
# exit()
# 重采样
rule_type = '5T'

period_df = df.resample(rule=rule_type, on='candle_begin_time', label='left', closed='left').agg({
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum',
})

period_df.dropna(subset=['open'], inplace=True)
period_df = period_df[period_df['volume'] > 0]
period_df.reset_index(inplace=True)
df = period_df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]

# 计算移动平均线
df['ma7'] = df['close'].rolling(7, min_periods=1).mean()
df['ma30'] = df['close'].rolling(30, min_periods=1).mean()

print(df)


