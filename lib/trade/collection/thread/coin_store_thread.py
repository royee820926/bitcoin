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
        exit()
        while True:
            total_volume = VolumeStore.get_total_volume()

            for coin_name, time_list in total_volume.items():
                is_not_empty = bool(time_list)
                if is_not_empty:
                    print(coin_name)
                    for base_timestamp, volume in time_list:
                        print(volume)

            time.sleep(0.5)
