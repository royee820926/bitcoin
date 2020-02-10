# encoding=utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import talib as ta
from lib.api.okex.spot_api import SpotApi
from datetime import datetime, timedelta

# print(help(ta.SMA))
# print(help(ta.MA))
print(pd.date_range('20000101', periods=100))
exit()

instrument_id = 'BTC-USDT'
kline = SpotApi.get_kline(instrument_id)

# for item in kline:
#     print(item)

df = pd.DataFrame(kline, columns={'candle_begin_time': 0, 'open': 1, 'high': 2, 'low': 3, 'close': 4, 'volume': 5})
df['candle_begin_time'] = df['candle_begin_time'].apply(lambda x: datetime.strftime(datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=8), '%Y-%m-%d %H:%M:%S'))

# sma
df['sma'] = ta.SMA(df['close'], timeperiod=5)

print(df)
exit()
