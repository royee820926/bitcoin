# encoding=utf-8

class RuntimeStatus:
    """
    运行时状态机
    每个时间级别下对应一个对象
    """
    ###################
    # 基本参数
    ###################
    # 币种名称
    _instrument_id = ''

    _df = None

    # 当前价格
    _price = ''

    ###################
    # 指标类参数
    ###################

    # macd柱线量化值（单边累加值）
    # candle_begin_time: [height, width]
    # 需要在相同
    _macd_bar = {}

    # 记录极值的变化
    # candle_begin_time: rsi6
    _rsi6 = {}

    # K线形态
    # 末尾一条K线的时间
    # {'candle_begin_time': 1} 值为对方向的预判和评分，评分为1 - 3，正数看多，负数看空
    k_form = {}

    def __init__(self, instrument_id, df):
        self._instrument_id = instrument_id
        self._df = df


