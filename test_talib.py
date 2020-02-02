# encoding=utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import talib

real0 = np.random.normal(10, 10, 10)[:2]
real1 = np.random.rand(10)[:2]
print(real0)
print(real1)

print(talib.ADD(real0, real1))

a = talib.EMA(real0, timeperiod=100)
b = talib.EMA(real1, timeperiod=100)

plt.figure()
plt.plot()
plt.show()


