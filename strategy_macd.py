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

# 先复制第一行的ema12和ema26为收盘价（shift(1)：上一条）
df['ema12'] = 0.0
df['ema26'] = 0.0

# 后面从第二行开始计算
for index, row in df.iterrows():
    if index == 0:
        # 先初始化第一行ema12和ema26
        prev_ema12 = df.at[0, 'ema12'] = df.at[0, 'close']
        prev_ema26 = df.at[0, 'ema26'] = df.at[0, 'close']
    else:
        prev_ema12 = df.at[index, 'ema12'] = (row['close'] * 2 + (12 - 1) * prev_ema12) / (12 + 1)
        prev_ema26 = df.at[index, 'ema26'] = (row['close'] * 2 + (26 - 1) * prev_ema26) / (26 + 1)

# df.loc[df['ema12'] == 0, 'ema12'] = (df['close'] * 2 + (12 - 1) * df['ema12'].shift(1)) / (12 + 1)
# df.loc[df['ema26'] == 0, 'ema26'] = (df['close'] * 2 + (26 - 1) * df['ema26'].shift(1)) / (26 + 1)

df['diff']  = df['ema12'] - df['ema26']
df['dea']   = df['diff'].rolling(9, min_periods=1).mean()
# macd柱线
df['macd_bar']  = (df['diff'] - df['dea']) * 2

# 交易量移动平均线
df['vma5']  = df['volume'].rolling(5, min_periods=1).mean()
df['vma10'] = df['volume'].rolling(10, min_periods=1).mean()

# print(df[['candle_begin_time', 'close', 'ma7', 'ma30', 'ema12', 'ema26', 'diff', 'dea', 'macd_bar', 'volume', 'vma5', 'vma10']])
# exit()

# ==== 标记信号 ====
# 做多

# 做多平仓

# 做空

# 做空平仓

# ====合并做多做空信号，去除重复信号
# df['signal'] = df[['signal_long', 'signal_short']].sum(axis=1)
# 如果pandas版本最新，使用下面代码和视频保持一致。
# min_count的意思是指定 NaN 个最少个数为1 超过1个NaN 就不计算 所以不会出现0.0
# df['signal'] = df[['signal_long', 'signal_short']].sum(axis=1, min_count=1, skipna=True)


# temp = df[df['signal'].notnull()][['signal']]
# print(temp.iloc[0: 10])

# temp = temp[temp['signal'] != temp['signal'].shift(1)]
# print(temp.iloc[0: 10])
# exit()
# df['signal'] = temp['signal']
# print(df[['candle_begin_time', 'signal']])
# exit()

# 删除中间列
# df.drop(['median', 'std', 'upper', 'lower', 'signal_long', 'signal_short'], axis=1, inplace=True)

# ====由signal计算出实际每天持有的仓位
# signal的计算运用了收盘价，是每根K线收盘之后产生的信号，到第二根开盘的时候才买入，仓位才会改变。
# df['pos'] = df['signal'].shift()
# df['pos'].fillna(method='ffill', inplace=True)
# df['pos'].fillna(value=0, inplace=True)     # 将初始行数的position补全为0

# print(df)

# ====将数据存入hdf文件中
# df.to_hdf('output/eth_bolling_signal.h5',
#           key='all_data', mode='w')
