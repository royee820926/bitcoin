# encoding=utf-8

from lib.pandas_module import PandasModule


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
    __original_data_frame = None
    __5t_data_frame = None


    def __init__(self, instrument_id, data_frame):
        self.__instrument_id = instrument_id
        self.__original_data_frame = data_frame

    def get_data_frame(self):
        """
        原始DataFrame
        :return:
        """
        return self.__original_data_frame

    def set_data_frame(self, df, deep=False):
        """
        原始DataFrame
        :param df:
        :param deep:
        :return:
        """
        self.__original_data_frame = df.copy(deep=deep)

    def get_5t_data_frame(self):
        """
        获取5分钟级别的DataFrame
        :return:
        """
        if self.__5t_data_frame is None:
            if self.__original_data_frame is None:
                raise Exception('Original data frame is none.')
            self.__5t_data_frame = PandasModule.resample(df=self.__original_data_frame, rule_type='5T')
        return self.__5t_data_frame




