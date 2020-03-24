# encoding=utf-8

import pandas as pd
from .input_parameter import InputParameter


class SpotTradeTest:
    """
    现货交易资金曲线测试
    """
    # 更新间隔时间（秒）
    _update_interval = 86400

    # 手续费
    _c_rate = 2.0 / 1000
    # 最低保证金比例（如：占到借来资产的15%）
    _min_margin_rate = 0.15
    # 总金额（现价 x 杠杆倍数）
    _total_cash = 0
    # 最低保证金
    _min_margin = 0

    @classmethod
    def init_param(cls, df):
        """
        初始化参数
        :param df: 依赖值: signal_lp, signal_ls
        :return:
        """
        df['signal'] = df[['signal_lp', 'signal_ls']].sum(axis=1, min_count=1, skipna=True)
        # 去除重复信号
        temp = df[df['signal'].notnull()][['signal']]
        temp = temp[temp['signal'] != temp['signal'].shift(1)]
        df['signal'] = temp['signal']
        df.drop(['signal_lp', 'signal_ls'], axis=1, inplace=True)

        # 由signal计算出实际每天持有的仓位
        df['pos'] = df['signal'].shift()
        # 向下（时间的前进方向）补全pos
        df['pos'].fillna(method='ffill', inplace=True)
        # 将初始行数的pos补全为0
        df['pos'].fillna(value=0, inplace=True)

        # ==== 计算涨跌幅
        # 根据收盘价计算涨跌幅（标准涨跌幅）
        df['change'] = df['close'].pct_change(1)
        # 从今天开盘买入，到今天收盘的涨跌幅（建仓买入时，使用的涨跌幅）
        df['buy_at_open_change'] = df['close'] / df['open'] - 1
        # 从今天收盘到明天开盘的涨跌幅（平仓时，使用的涨跌幅）
        df['sell_next_open_change'] = df['open'].shift(-1) / df['close'] - 1
        # sell_next_open_change最后一条数据补全为零，可视为下一K线的开盘价和上一K线的收盘价相同
        df.at[len(df) - 1, 'sell_next_open_change'] = 0

        df.reset_index(inplace=True, drop=True)

    @classmethod
    def get_total_cash(cls, init_cash, leverage_rate):
        """
        获取总现金（现金 x 杠杆倍数）
        :param init_cash 现金
        :param leverage_rate 杠杆倍数
        :return:
        """
        return init_cash * leverage_rate

    @classmethod
    def get_min_margin(cls, init_cash, leverage_rate, min_margin_rate):
        """
        获取最低保证金
        :param init_cash
        :param leverage_rate
        :param min_margin_rate
        :return:
        """
        return init_cash * leverage_rate * min_margin_rate

    @classmethod
    def money_curve(cls, df, init_cash=1000, leverage_rate=3):
        """
        计算资金曲线
        :param df:
        :param init_cash: 初始资金
        :param leverage_rate: 杠杆倍数
        :param
        :return:
        """
        # 初始化DataFrame参数
        cls.init_param(df=df)

        # 手续费
        c_rate = cls._c_rate
        # 最低保证金率
        min_margin_rate = 0 # cls._min_margin_rate
        # 总的杠杆金额
        total_cash = cls.get_total_cash(init_cash, leverage_rate)
        # 最低保证金
        min_margin = cls.get_min_margin(init_cash, leverage_rate, min_margin_rate)

        # 开仓的条件
        condition1 = df['pos'] != 0
        condition2 = df['pos'] != df['pos'].shift(1)
        open_pos_condition = condition1 & condition2

        # 平仓的条件
        condition1 = df['pos'] != 0
        condition2 = df['pos'] != df['pos'].shift(-1)
        close_pos_condition = condition1 & condition2

        # ==== 对每次交易进行分组
        # start_time 为开仓的行
        df.loc[open_pos_condition, 'start_time'] = df['candle_begin_time']
        # 向下补全（向时间前进的方向）
        df['start_time'].fillna(method='ffill', inplace=True)
        # 将pos=0（不持仓）的行，start_time设置为pd.NaT
        df.loc[df['pos'] == 0, 'start_time'] = pd.NaT

        # ===计算仓位变动
        # 建仓后的仓位
        df.loc[open_pos_condition, 'position'] = total_cash * (1 + df['buy_at_open_change'])

        # 开仓后每天的仓位的变动
        group_num = len(df.groupby('start_time'))
        if group_num > 1:
            t = df.groupby('start_time').apply(lambda x: x['close'] / x.iloc[0]['close'] * x.iloc[0]['position'])
            # level=[0] : 把索引列中start_time一列去掉，只剩下自然索引列
            t = t.reset_index(level=[0])
            # 将计算结果的close列赋值到df['position']
            df['position'] = t['close']
        # elif group_num == 1:
        #     t = df.groupby('start_time')[['close', 'position']].apply(lambda x: x['close'] / x.iloc[0]['close'] * x.iloc[0]['position'])
        #     df['position'] = t.T.iloc[:, 0]

        # 每根K线仓位的最大值和最小值，针对最高价和最低价
        df['position_max'] = df['position'] * df['high'] / df['close']
        df['position_min'] = df['position'] * df['low'] / df['close']

        # 平仓时仓位（最后一条做多记录的position，以下一行数据的涨幅比例计算平仓价格）
        df.loc[close_pos_condition, 'position'] *= (1 + df.loc[close_pos_condition, 'sell_next_open_change'])

        # ===计算每天实际持有资金的变化
        # 计算持仓利润
        df['profit'] = (df['position'] - total_cash) * df['pos']  # 持仓盈利或者损失

        # 计算持仓利润最小值
        df.loc[df['pos'] == 1, 'profit_min'] = (df['position_min'] - total_cash) * df['pos']  # 最小持仓盈利或者损失
        df.loc[df['pos'] == -1, 'profit_min'] = (df['position_max'] - total_cash) * df['pos']  # 最小持仓盈利或者损失

        # 计算实际资金量
        df['cash'] = init_cash + df['profit']  # 实际资金
        df['cash'] -= total_cash * c_rate  # 减去建仓时的手续费
        df['cash_min'] = df['cash'] - (df['profit'] - df['profit_min'])  # 实际最小资金
        df.loc[close_pos_condition, 'cash'] -= df.loc[close_pos_condition, 'position'] * c_rate  # 减去平仓时的手续费

        # ===判断是否会爆仓
        # 如果存在df['cash_min'] <= min_margin的
        _index = df[df['cash_min'] <= min_margin].index
        if len(_index) > 0:
            print('有爆仓 X %s' % len(_index))
            df.loc[_index, '强平'] = 1
            # 在持仓分组内，将强平余下的行也设置为1，因为已经没有用
            df['强平'] = df.groupby('start_time')['强平'].fillna(method='ffill')
            # 将第一次出现强平的行标记出来
            df.loc[(df['强平'] == 1) & (df['强平'].shift(1) != 1), 'cash_强平'] = df['cash_min']  # 此处是有问题的
            # 将出现强平信号的行的cash设置为None
            df.loc[(df['pos'] != 0) & (df['强平'] == 1), 'cash'] = None
            # 将爆仓的行用cash_强平 来补充cash值
            df['cash'].fillna(value=df['cash_强平'], inplace=True)
            # 在分组中，将cash为空的值（出现爆仓的行）向前补全
            df['cash'] = df.groupby('start_time')['cash'].fillna(method='ffill')
            # 删除不必要的数据
            df.drop(['强平', 'cash_强平'], axis=1, inplace=True)

        # ===计算资金曲线
        # equity_change 每天的涨跌幅
        df['equity_change'] = df['cash'].pct_change()
        # 重新计算开仓时的equity_change （每日涨跌幅）
        df.loc[open_pos_condition, 'equity_change'] = df.loc[open_pos_condition, 'cash'] / init_cash - 1  # 开仓日的收益率
        # 没有持仓，equity_change补全为0
        df['equity_change'].fillna(value=0, inplace=True)
        # 将equity_change连乘起来
        df['equity_curve'] = (1 + df['equity_change']).cumprod()

        # ===删除不必要的数据
        df.drop(['change', 'buy_at_open_change', 'sell_next_open_change', 'start_time', 'position', 'position_max',
                 'position_min', 'profit', 'profit_min', 'cash', 'cash_min'], axis=1, inplace=True)




