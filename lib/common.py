# encoding=utf-8


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
