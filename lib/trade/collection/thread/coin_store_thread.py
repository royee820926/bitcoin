# encoding=utf-8

import threading
import time
from lib.trade.collection.volume_store import VolumeStore
from lib.db.mongo_handler import MongoHandle


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
                    # 当前时间戳
                    current_time = int(time.time())
                    interval = 600  # 间隔10分钟

                    # 遍历各个时间节点的统计
                    for base_timestamp, volume in time_list.items():
                        # 1 删除10分钟前的数据
                        # 2 如果数据库中存在该时间戳的记录，则将成绩量写入数据库，
                        # 3 否则略过该条数据，

                        if current_time - base_timestamp >= interval:
                            # 删除base_timestamp对应的数据
                            VolumeStore.del_volume_by_timestamp(coin_name, base_timestamp)

                        col = MongoHandle.get_spot_collection(coin_name)
                        condition = {
                            'time': int(base_timestamp)
                        }
                        doc = col.find_one(condition)

                        # 交易量计算
                        # 赋值后清空 symbol='0'
                        VolumeStore.get_lock().acquire()
                        volume = VolumeStore.volume_set_volume(coin_name, base_timestamp, symbol='0')
                        VolumeStore.get_lock().release()

                        buy_volume = volume.get('buy_volume', 0)
                        sell_volume = volume.get('sell_volume', 0)
                        if buy_volume == 0 and sell_volume == 0:
                            # 都为0，则跳过
                            continue

                        if 'buy_volume' in doc:
                            buy_volume += float(doc['buy_volume'])
                        if 'sell_volume' in doc:
                            sell_volume += float(doc['sell_volume'])
                        update_data = {'buy_volume': buy_volume, 'sell_volume': sell_volume}

                        # 更新成交量
                        result = col.update_one({'time': int(base_timestamp)}, {'$set': update_data})

            time.sleep(0.5)
