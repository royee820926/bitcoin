# encoding=utf-8

import threading
import time
from lib.trade.collection.volume_store import VolumeStore


class CoinStoreThread(threading.Thread):
    """
    采集数据存储
    """
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self, name=name)
        self.threadID = thread_id

    def run(self):
        while True:
            # 获取1分钟成交数据
            total_volume = VolumeStore.get_total_volume()
            # 遍历现货（或合约等）不同的币种
            for coin_name, time_list in total_volume.items():
                is_not_empty = bool(time_list)
                # 如果该币种存在统计结果
                if is_not_empty:
                    # 遍历各个时间节点的统计
                    for base_timestamp, volume in time_list.items():
                        # 如果数据库中存在该时间戳的记录，则将成绩量写入数据库，
                        # 否则略过该条数据，
                        # 删除10分钟前的数据
                        pass
                        # print(coin_name)
                        # print(base_timestamp)
                        # print(volume)
                        # exit()

            time.sleep(0.5)
