# encoding=utf-8
# 1分钟合约K线数据
# 数据库 okex_swap

from lib.api.okex.swap_api import SwapApi
from config.swap_coin import swap_coin_type
from lib.db.mongo_handler import get_swap_collection
from lib.okex.exceptions import OkexAPIException
import time
import threading
import requests


class SwapThread(threading.Thread):
    """
    多线程请求，写入数据
    """

    # 最大读取秒数
    _max_backward_second = 2000 * 60
    # K线接口返回的最大条数
    _max_once_size = 200

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def need_joining(self):
        """
        当数据库最后一条数据离开当前时间超过200分钟，
        即一次请求无法填补空缺数据，需要完全查找时间点
        :return:
        """
        instrument_id = self.name
        # 当前时间戳（秒）
        current = int(time.time())

        # 获取最后一条K线数据
        last_result = collection_dict[instrument_id].find().sort([('time', -1)]).limit(1)
        try:
            # 数据表中没有数据，last_timestamp设置为0
            last_result = last_result.next()
            last_timestamp = int(last_result['time'])

            if current - last_timestamp >= self._max_backward_second:
                start_stamp = current - self._max_backward_second
            elif current - last_timestamp < (self._max_once_size * 60):
                # 小于最大返回条数的时间，则不需要拼接
                return 0
            else:
                start_stamp = last_timestamp
        except StopIteration:
            # 如果没有数据，则找2000分钟前的K线数据（最多往前找2000分钟）
            # 减去2000分钟的秒数
            start_stamp = current - self._max_backward_second
        return start_stamp

    def spider(self, start_stamp='', end_stamp=''):
        """
        采集并写入数据主体
        :return:
        """
        try:
            # 获取K线接口1分钟数据
            instrument_id = self.name

            if start_stamp != '' and end_stamp != '':
                start_stamp = time.strftime('%Y-%m-%dT%H:%M:00.000Z', time.localtime(start_stamp))
                end_stamp   = time.strftime('%Y-%m-%dT%H:%M:00.000Z', time.localtime(end_stamp))
            else:
                start_stamp = ''
                end_stamp = ''
            kline_data = SwapApi.get_kline(instrument_id, start=start_stamp, end=end_stamp)

            # 数据长度
            kline_len = len(kline_data)
            count = 0

            for kline_item in kline_data:
                count += 1
                # 最后一个可能是不完整的一分钟，不写入，下一次读取再判断
                if count == kline_len:
                    print('break....')
                    break
                # 转换ISO 8601 为时间戳
                k_time = kline_item[0]
                try:
                    time_array = time.strptime(k_time, "%Y-%m-%dT%H:%M:%S.000Z")
                except ValueError:
                    # 日期模式匹配失败
                    print(instrument_id)
                    print('continue 1....')
                    continue

                # 东八区时间
                timestamp = int(time.mktime(time_array)) + 8 * 60 * 60

                # 检查该时间戳的K线是否已经写入
                last_result = collection_dict[instrument_id].find().sort([('time', -1)]).limit(1)

                try:
                    # 数据表中没有数据，last_timestamp设置为0
                    last_result = last_result.next()
                    last_timestamp = int(last_result['time'])
                except StopIteration:
                    last_timestamp = 0

                # 如果timestamp小于等于最后一条记录的时间戳，则跳过
                if timestamp <= last_timestamp:
                    print('continue 2....')
                    continue

                # 收集数据
                k_open = kline_item[1]
                k_high = kline_item[2]
                k_low = kline_item[3]
                k_close = kline_item[4]
                k_volume = kline_item[5]
                document = {
                    # 东八区时间
                    "time": int(timestamp),
                    "open": float(k_open),
                    "high": float(k_high),
                    "low": float(k_low),
                    "close": float(k_close),
                    "volume": float(k_volume)
                }
                # 写入数据
                inserted_id = collection_dict[instrument_id].insert_one(document).inserted_id
                print('%d.......' % timestamp)
                document['inserted_id'] = inserted_id

        except requests.exceptions.SSLError as rse:
            # 请求错误
            time.sleep(5)
            print(rse)
            print('requests.exceptions.SSLError after 5 second!')

        except requests.exceptions.ConnectionError as rce:
            # 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。
            time.sleep(5)
            print(rce)
            print('requests.exceptions.ConnectionError after 5 second!')

        except requests.exceptions.ReadTimeout as rto:
            # 读请求超时
            time.sleep(5)
            print(rto)
            print('requests.exceptions.ReadTimeout after 5 second!')

        except requests.exceptions.ConnectTimeout as cto:
            # 连接请求超时
            time.sleep(5)
            print(cto)
            print('requests.exceptions.ConnectTimeout after 5 second!')

        except OkexAPIException as oae:
            time.sleep(5)
            # 可能错误
            # Invalid JSON error
            print(oae)
            print('okex.exceptions.OkexAPIException')

    def run(self):
        """
        构造函数
        :return:
        """
        instrument_id = self.name
        current = int(time.time())

        # 当数据库最后一条数据离开当前时间超过200分钟，
        # 即一次请求无法填补空缺数据，需要完全查找时间点
        start_stamp = self.need_joining()

        # 尽量补全前面的记录
        if start_stamp > 0:
            index = 1
            while True:
                ##############################
                print('before...%d' % index)
                index += 1
                ##############################
                end_stamp = start_stamp + self._max_once_size * 60
                self.spider(start_stamp, end_stamp)
                # 下一次开始（start包含，end不包含）
                start_stamp = end_stamp

                # 判断退出
                if current - start_stamp < self._max_once_size * 60:
                    # 时间间隔小于 _max_once_size
                    break

        while True:
            # 正式执行
            self.spider()

            # 睡眠1分钟
            print('===============睡眠60秒===============')
            time.sleep(60)


# 初始化集合对象
collection_dict = {}
for coin_name in swap_coin_type:
    collection_dict[coin_name] = get_swap_collection(coin_name)

thread_dict = {}
thread_index = 0

################################################
# 测试单个
# swap_obj = SwapThread(1, 'BTC-USDT', 1)
# swap_obj.run()
# exit(1)
################################################

for coin_name in swap_coin_type:
    # 每个coin启动一个线程 #
    ######################
    thread_index += 1
    thread_dict[coin_name] = SwapThread(thread_index, coin_name, thread_index)
    # 设置守护线程
    thread_dict[coin_name].setDaemon(True)
    # 启动线程
    thread_dict[coin_name].start()
    print('启动线程: %d, 名字: %s' % (thread_index, coin_name))
print('===================================')
# 阻塞线程
for coin_name in swap_coin_type:
    print('阻塞线程start: %s' % coin_name)
    thread_dict[coin_name].join()
    print('阻塞线程end: %s' % coin_name)

print('主线程退出')
