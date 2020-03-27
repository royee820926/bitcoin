# encoding=utf-8

from lib.db.mongo_handler import get_spot_collection

import pandas as pd
import talib as ta
import time
from lib.strategy.long_position import LongPositionStrategy as lps
from lib.strategy.long_selling import LongSellingStrategy as lss

from lib.pandas_module import PandasModule

# 初始化pandas参数
PandasModule.init(pd=pd)

instrument_id = 'BTC-USDT'
# instrument_id = 'EOS-USDT'
# instrument_id = 'ETH-USDT'

start_time = int(time.time()) - 2 * 24 * 60 * 60
kline_length = 2 * 24 * 60
result = PandasModule.get_data_from_mongo(instrument_id, start_time=start_time, kline_length=kline_length)

df = pd.DataFrame(result)
df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'], format='%Y-%m-%d %H:%M:%S')
# print(type(df.iloc[0]['candle_begin_time']))
# exit()
# 重采样
kline_rule = 5
df = PandasModule.resample(df, kline_rule=kline_rule)

# 计算移动平均线
# df['ma7']  = df['close'].rolling(7, min_periods=1).mean()
# df['ma20'] = df['close'].rolling(20, min_periods=1).mean()
# df['ma30'] = df['close'].rolling(30, min_periods=1).mean()
df['ma60'] = df['close'].rolling(60, min_periods=1).mean()

# TA-Lib -> MACD
df['dif'], df['dea'], df['macd_bar'] = ta.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)

# TA-Lib -> RSI
df['rsi6'] = ta.RSI(df['close'], timeperiod=6)
df['rsi12'] = ta.RSI(df['close'], timeperiod=12)
df['rsi24'] = ta.RSI(df['close'], timeperiod=24)

# 交易量移动平均线
# df['vma5']  = df['volume'].rolling(5, min_periods=1).mean()
# df['vma10'] = df['volume'].rolling(10, min_periods=1).mean()

# print(df[['candle_begin_time', 'close', 'median', 'std', 'upper', 'lower']])

# boll指标
from lib.indicator.boll_indicator import BollIndicator
BollIndicator.get_value(df=df)

# obv指标
from lib.indicator.obv_indicator import ObvIndicator
ObvIndicator.get_value(df=df)

# ==== 标记信号 ====
# 做多信号
# lps.lower_rsi_next(df=df)
# lps.macd_upward_through(df=df)
lps.boll_upward_through(df=df)

# 做多平仓信号
# lss.find_rsi_top(df=df)
lss.boll_downward_through(df=df)
# print(df[['candle_begin_time', 'close', 'rsi6', 'signal_lp', 'signal_ls']])
# exit()

# ==== 计算资金 ====
from test.spot_trade_test import SpotTradeTest

SpotTradeTest.money_curve(df=df, init_cash=1000, leverage_rate=30)

# print(df[['candle_begin_time', 'close', 'rsi6', 'signal', 'pos', 'equity_change', 'equity_curve']])
print(df)
# print(df[df['signal'].notnull()])
exit()

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

print(df)
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
