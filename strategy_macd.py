# encoding=utf-8

from lib.db.mongo_handler import get_spot_collection
from lib.api.okex.spot_api import SpotApi
import pandas as pd
import talib as ta
import time

# 不换行显示
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
# pd.set_option('display.max_rows', None)

# instrument_id = 'BTC-USDT'
# instrument_id = 'EOS-USDT'
instrument_id = 'ETH-USDT'
collection = get_spot_collection(instrument_id)

# 取出多少条1分钟K线（选取2天的K线前导数据，diff和dea计算结果会趋于为固定值）
kline_length = 2 * 24 * 60
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
kline_rule = 5
rule_type = '%dT' % kline_rule

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
# df['ma7']  = df['close'].rolling(7, min_periods=1).mean()
# df['ma20'] = df['close'].rolling(20, min_periods=1).mean()
# df['ma30'] = df['close'].rolling(30, min_periods=1).mean()
# df['ma60'] = df['close'].rolling(60, min_periods=1).mean()

# TA-Lib -> RSI
# df['dif'], df['dea'], df['macd_bar'] = ta.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)

# TA-Lib -> RSI
df['rsi6'] = ta.RSI(df['close'], timeperiod=6)
df['rsi12'] = ta.RSI(df['close'], timeperiod=12)
df['rsi24'] = ta.RSI(df['close'], timeperiod=24)
# df['fastk'], df['fastd'] = ta.STOCHRSI(df['close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
print(df)
exit()




# 交易量移动平均线
# df['vma5']  = df['volume'].rolling(5, min_periods=1).mean()
# df['vma10'] = df['volume'].rolling(10, min_periods=1).mean()

# BOLL指标
n = 20     # 中轨n根K线的移动平均线
m = 2      # 系数
# 计算中轨
df['median'] = df['close'].rolling(n, min_periods=1).mean()
# 计算标准差
df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)  # ddof 标准差自由度
# 计算上轨
df['upper'] = df['median'] + m * df['std']
# 计算下轨
df['lower'] = df['median'] - m * df['std']
# print(df[['candle_begin_time', 'close', 'median', 'std', 'upper', 'lower']])
# exit()

# OBV指标（能量潮）
# for index, row in df.iterrows():
#     if index == 0:
#         prev_obv = df.at[0, 'obv'] = 0
#     else:
#         if df.at[index, 'close'] > prev_obv:
#             prev_obv = df.at[index, 'obv'] = prev_obv + df.at[index, 'volume']
#         elif df.at[index, 'close'] < prev_obv:
#             prev_obv = df.at[index, 'obv'] = prev_obv - df.at[index, 'volume']
#         else:
#             prev_obv = df.at[index, 'obv'] = prev_obv
# print(df.tail(40))
# exit()

# RSI指标
# df['rsi1']
# df['rsi2']
# df['rsi3']

# KDJ指标

# print(df.tail(40))
# exit()

# print(df[['candle_begin_time', 'close', 'ma7', 'ma30', 'ema12', 'ema26', 'dif', 'dea', 'macd_bar', 'volume', 'vma5', 'vma10']])
# exit()

# ==== 标记信号 ====
# [2：做多、1：做多平仓、-2：做空、-1：做空平仓]

# 做多信号1
# DIF上穿DEA
# dif_cond1 = df['dif'] > df['dea']
# dif_cond2 = df['dif'].shift(1) <= df['dea'].shift(1)
# # MACD由负变正
# bar_cond1 = df['macd_bar'] > df['macd_bar'].shift(1)
# bar_cond2 = df['macd_bar'] > 0
# bar_cond3 = df['macd_bar'].shift(1) <= 0
# # K线收盘价在布林线中轨的下方
# boll_cond1 = df['close'] < df['median']
# df.loc[dif_cond1 & dif_cond2 & bar_cond1 & bar_cond2 & bar_cond3 & boll_cond1 , 'signal_up'] = 2

# 做多信号2(recommend)
# # dif从下往上接近dea
# dif_cond1 = df['dif'] < df['dea']
# dif_cond2 = df['dea'] - df['dif'] < 0.002
# dif_cond3 = df['dif'].shift(1) < df['dea'].shift(1)
# # macd柱线由弱转强，柱线图向下深度连续两根小于-0.015
# macd_cond1 = df['macd_bar'] > df['macd_bar'].shift(1)
# macd_cond2 = df['macd_bar'].shift(1) < df['macd_bar'].shift(2)
# macd_cond3 = df['macd_bar'].shift(2) < -0.015
# line_cond1 = df['close'] < df['ma60']
# df.loc[((dif_cond1 & dif_cond2 & dif_cond3) | (macd_cond1 & macd_cond2 & macd_cond3)) & line_cond1, 'signal_up'] = 2

# RSI做多信号(6, 12, 24)
for index, row in df.iterrows():
    if index == 0:
        continue

    up_sum = 0
    down_sum = 0
    up_count = 0
    down_count = 0
    start_index = -1
    # RS6
    if index - start_index > 6:
        start_index = index - 6
    for ii in range(index, start_index, -1):
        # c_index 相对区间位置索引
        c_index = index - ii
        if c_index == 0:
            continue
        try:
            if df.at[c_index, 'close'] > df.at[c_index-1, 'close']:
                up_sum += (df.at[c_index, 'close'] - df.at[c_index-1, 'close'])
                up_count += 1
            elif df.at[c_index, 'close'] < df.at[c_index-1, 'close']:
                down_sum += (df.at[c_index-1, 'close'] - df.at[c_index, 'close'])
                down_count += 1
        except KeyError:
            print('error:')
            print(index)
            print(ii)
            print(c_index)
            exit()
    if up_sum == 0 or down_sum == 0:
        df.at[0, 'rs6'] = 0
    else:
        df.at[0, 'rs6'] = (up_sum / up_count) / (down_sum / down_count)


df['rsi6'] = 100 - (100 / (1 + df['rs6']))
print(df)
# print(df[['candle_begin_time', 'close', 'ma60', 'dif', 'dea', 'macd_bar', 'signal_up']])
exit()

# 做空
dif_cond1 = df['dif'] < df['dif'].shift(1)
dif_cond2 = df['dif'].shift(1) > df['dif'].shift(2)
df.loc[dif_cond1 & dif_cond2, 'signal_dn'] = -2
print(df[['candle_begin_time', 'close', 'ma60', 'dif', 'dea', 'macd_bar', 'signal_up', 'signal_dn']])
exit()

# 做多平仓
# 做空平仓

print(df)
exit()
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
