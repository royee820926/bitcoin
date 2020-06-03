# encoding=utf-8

class Runtime:
    """
    运行时状态机
    每个时间级别下对应一个对象
    """
    ###################
    # 基本参数
    ###################
    # 币种名称
    __instrument_id = ''
    # DataFrame
    __df = None

    # def __init__(self, instrument_id, df):
    #     self.__instrument_id = instrument_id
    #     self.__df = df

    @classmethod
    def k_line_form(cls, df):
        """
        K线形态
        :param df:
        :return:
        """



