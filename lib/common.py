# encoding=utf-8

import time
import datetime


def get_dict(value, *param):
    """
    根据名字获取字典内容
    dict['aaa']['bbb']['ccc']
    调用: get_dict(dict, 'aaa', 'bbb', 'ccc')
    :param value:
    :param param:
    :return:
    """
    result = value
    for name in param:
        if name in result:
            result = result[name]
        else:
            return None
    return result


class TimeOption:
    @classmethod
    def string2datetime(cls, time_str, format_str, hours=0):
        """
        字符串转换为datetime
        :param time_str:
        :param format_str:
        :param hours:
        :return:
        """
        time_array = datetime.datetime.strptime(time_str, format_str)
        # 转换时区加减时间
        if hours != 0:
            time_array = time_array + datetime.timedelta(hours=hours)
        return time_array

    @classmethod
    def string2timestamp(cls, time_str, format_str, hours=0):
        """
        字符串转换为时间戳
        :param time_str:
        :param format_str:
        :param hours:
        :return:
        """
        time_array = cls.string2datetime(time_str, format_str, hours)
        return time.mktime(time_array.timetuple())

    @classmethod
    def datetime2timestamp(cls, time_array):
        """
        datetime转换为时间戳
        :param time_array:
        :return:
        """
        return time.mktime(time_array.timetuple())

    @classmethod
    def set_datetime(cls, time_array, **params):
        """
        设置datetime
        :param time_array:
        :param params:
        :return:
        """
        for key, val in params.items():
            if key == 'second':
                time_array = time_array.replace(second=val)
        return time_array
