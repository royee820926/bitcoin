# encoding=utf-8

import time
from lib.db.mongo_handler import get_spot_collection
from lib.db.mongo_handler import MongoHandle
from lib.common import TimeOperation
from lib.api.okex.spot_api import SpotApi
import pandas as pd

class PandasModule:
    @classmethod
    def init(cls):
        """
        初始化pandas参数
        :return:
        """
        # 不换行显示
        pd.set_option('expand_frame_repr', False)
        # pd.set_option('display.max_rows', 100)
        # pd.set_option('display.min_rows', 100)
        pd.set_option('display.max_rows', None)

    @classmethod
    def get_data_from_mongo(cls, instrument_id, start_time, kline_length=2*24*60):
        """
        从数据库中获取现货数据（默认倒序）
        :param instrument_id:
        :param start_time: 开始时间戳
        :param kline_length: K线数据的分钟数（默认2天）
        :return:
        """
        result = []
        collection = get_spot_collection(instrument_id)
        temp = collection.find({"time": {"$gte": int(start_time)}}).sort([('time', -1)]).limit(kline_length)
        last_stamp_zh = 0

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
        return result

    @classmethod
    def get_swap_from_mongo(cls, instrument_id, start_time=0, end_time=0, kline_length=2 * 24 * 60, as_df=True):
        """
        从数据库中获取合约数据（默认倒序）
        :param instrument_id:
        :param start_time: 开始时间戳
        :param end_time: 结束时间戳（下不包含）
        :param kline_length: K线数据的分钟数（默认2天）
        :param as_df: 获取结果后，是否转换成DataFrame
        :return:
        """
        result = []
        limit = 0
        time_sort = 1
        collection = MongoHandle.get_swap_collection(instrument_id)

        # 判断查询条件和返回条数
        if start_time != 0 and end_time != 0:
            condition = {"time": {"$gte": int(start_time), "$lt": int(end_time)}}
        elif start_time != 0:
            condition = {"time": {"$gte": int(start_time)}}
            limit = kline_length
        elif end_time != 0:
            condition = {"time": {"$lt": int(end_time)}}
            limit = kline_length
            time_sort = -1
        else:
            # 没有开始结束时间，则end_time为当前时间戳
            end_time = int(time.time())
            condition = {"time": {"$lt": int(end_time)}}
            limit = kline_length
            time_sort = -1

        temp = collection.find(condition).sort([('time', time_sort)])
        if limit > 0:
            temp = temp.limit(kline_length)
        # 添加结果
        for item in temp:
            result.append({
                'candle_begin_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['time'])),
                'open': float(item['open']),
                'high': float(item['high']),
                'low': float(item['low']),
                'close': float(item['close']),
                'volume': float(item['volume']),
            })
        if time_sort == -1:
            result = list(reversed(result))

        # 判断是否需要转换成DataFrame
        if as_df:
            df = pd.DataFrame(result)
            df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'], format='%Y-%m-%d %H:%M:%S')
            return df
        return result

    @classmethod
    def append_one_swap_from_mongo(cls, instrument_id, df, start_time):
        """
        从MongoDB追加合约数据
        :param instrument_id:
        :param df: 结果存入DataFrame
        :param start_time: 读取记录的时间
        :return:
        """
        collection = MongoHandle.get_swap_collection(instrument_id)
        result = collection.find_one({"time": int(start_time)})

        if result is not None:
            data = {
                'candle_begin_time': TimeOperation.timestamp2string(result['time']),
                'open': float(result['open']),
                'high': float(result['high']),
                'low': float(result['low']),
                'close': float(result['close']),
                'volume': float(result['volume']),
            }
            return df.append(data, ignore_index=True)
        else:
            return None

    @classmethod
    def delete_first_one(cls, df):
        """
        DataFrame 删除第一条数据
        :param df:
        :return:
        """
        df.drop(index=0, inplace=True)
        df.reset_index(inplace=True, drop=True)
        # for item in df.iterrows():
        #     df_index = item[0]
        #     df.drop(index=df_index, inplace=True)
        #     break

    @classmethod
    def kline_complete(cls, instrument_id, result):
        """
        补全K线（即将废弃）
        :param instrument_id:
        :param result:
        :return:
        """
        last_stamp_zh = 0
        # 转换ISO8601
        # 加60秒掠过last_stamp
        last_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.localtime(last_stamp_zh + 60))
        # 从接口补全K线记录
        temp = SpotApi.get_kline(instrument_id, start=last_time)

        for item in temp:
            time_array = time.strptime(item[0], "%Y-%m-%dT%H:%M:%S.000Z")
            timestamp = time.mktime(time_array) + 8 * 3600
            candle_begin_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

            result.append({
                'candle_begin_time': candle_begin_time,
                'open': float(item[1]),
                'high': float(item[2]),
                'low': float(item[3]),
                'close': float(item[4]),
                'volume': float(item[5]),
            })

    @classmethod
    def resample(cls, df, rule_type=5):
        """
        重采样
        :param df:
        :param rule_type: （如：5T 5分钟K线）
        :return:
        """
        period_df = df.resample(rule=rule_type, on='candle_begin_time', label='left', closed='left').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum',
        })

        period_df.dropna(subset=['open'], inplace=True)
        period_df = period_df[period_df['volume'] > 0]
        period_df.reset_index(inplace=True)
        df = period_df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]
        return df
