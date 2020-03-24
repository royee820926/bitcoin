# encoding=utf-8

import time
from lib.db.mongo_handler import get_spot_collection

class PandasModule:
    @classmethod
    def init(cls, pd):
        """
        初始化pandas参数
        :param pd:
        :return:
        """
        # 不换行显示
        pd.set_option('expand_frame_repr', False)
        # pd.set_option('display.max_rows', 100)
        # pd.set_option('display.min_rows', 100)
        pd.set_option('display.max_rows', None)

    @classmethod
    def get_data_from_mongo(cls, instrument_id, kline_length=2*24*60):
        """
        从数据库中获取数据
        :param instrument_id:
        :param kline_length: K线数据的分钟数（默认2天）
        :return:
        """
        collection = get_spot_collection(instrument_id)
        temp = collection.find().sort([('time', -1)]).limit(kline_length)

        result = []
        for item in temp:
            if last_stamp_zh == 0:
                # 最后一条时间戳（请求kline接口时，换算成UTC时间）
                last_stamp_zh = int(item['time']) - 8 * 3600
            result.append({
                'candle_begin_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['time'])),
                'open': float(item['open']),
                'high': float(item['high']),
                'low': float(item['low']),
                'close': float(item['close']),
                'volume': float(item['volume']),
            })

        result = list(reversed(result))

