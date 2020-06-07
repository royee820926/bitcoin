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
    __level_data_frame = {}
    __level_list = []


    def __init__(self, instrument_id):
        self.__instrument_id = instrument_id

    def get_data_frame(self):
        """
        原始DataFrame
        :return:
        """
        return self.__original_data_frame

    def set_data_frame(self, df, level_list=[], deep=False):
        """
        原始DataFrame
        :param df:
        :param level_list: 例如：['5T']
        :param deep:
        :return:
        """
        self.__original_data_frame = df.copy(deep=deep)
        # 设置其他级别
        if bool(level_list):
            for level_type in level_list:
                self.set_level_data_frame(level_type, df)

    def get_level_data_frame(self, rule_type):
        """
        获取时间级别DataFrame
        :param rule_type:
        :return:
        """
        if rule_type in self.__level_data_frame:
            return self.__level_data_frame[rule_type]
        return None

    def set_level_data_frame(self, rule_type, df):
        """
        设置时间级别的DataFrame
        :param rule_type: 例如：5T
        :param df:
        :return:
        """
        self.__level_data_frame[rule_type] = PandasModule.resample(df=df, rule_type=rule_type)

    def start(self):
        """
        开始循环判断
        :return:
        """
        # 当前索引
        current_index = 0
        df = self.get_level_data_frame('5T')
        for item in df.iterrows():
            current_index = int(item[0])
            break
        while True:
            item = df.iloc[current_index]





