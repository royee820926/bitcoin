# encoding=utf-8

import re
from lib.indicator.boll_indicator import BollIndicator
from lib.indicator.macd_indicator import MacdIndicator
from lib.indicator.rsi_indicator import RsiIndicator
from lib.indicator.ma_indicator import MaIndicator


class BaseIndicator:
    """
    基础指标：
    涨幅，振幅...
    """

    @classmethod
    def increase(cls, df, interval=1):
        """
        涨幅
        :param df: 依赖值: open
        :param interval:
        :return:
        """
        df['increase'] = (df['open'] - df['open'].shift(interval)) / df['open'].shift(interval) * 100

    @classmethod
    def amplitude(cls, df):
        """
        振幅 = (当天的最高价格 - 最低价格） / 昨天收盘价格 * 100%
        :param df:
        :return:
        """
        pass
        # df['amplitude']

    @classmethod
    def rely_on_indicator(cls, df, ind_list=[]):
        """
        根据需要添加指标
        :param df:
        :param ind_list:
        :return:
        """
        if not isinstance(ind_list, list):
            return
        # dataframe 中的字段
        df_index = df.columns

        for ind_name in ind_list:
            # 如果指标不存在，则添加该指标
            if ind_name not in df_index:
                # ma5|ma10|ma20|ma60 等移动平均线
                if re.match(r'^ma\d{1,2}$', ind_name) is not None:
                    MaIndicator.get_value(df, ind_name)
                # 布林带
                if ind_name in ['boll_median', 'boll_upper', 'boll_lower']:
                    BollIndicator.get_value(df)
                # MACD
                if ind_name in ['dif', 'dea', 'macd_bar']:
                    MacdIndicator.get_value(df)
                # RSI
                if re.match(r'^rsi\d{1,2}$', ind_name) is not None:
                    RsiIndicator.get_value(df, ind_name)


