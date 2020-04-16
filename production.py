# encoding=utf-8
# python production.py --env=test
# python production.py --env=prod
# 生产环境
# 1、从接口获取数据
# 2、计算指标
# 3、计算买卖信号
# 4、发送邮件
# 5、记录日志

from lib.production.production import Production as prod
from lib.production.testing import Testing as test
import sys


if __name__ == '__main__':
    command = {
        'env': '',
    }
    index = 0
    for comm in sys.argv:
        if index == 0:
            index += 1
            continue
        comm = comm.replace('-', '')
        comm_list = comm.split('=')
        if len(comm_list) == 2 and comm_list[0] != '':
            command[comm_list[0]] = comm_list[1]

    if command['env'] == 'prod':
        prod.run()
    else:
        test.run()




