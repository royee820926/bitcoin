import requests
import json
from . import consts as c, utils, exceptions
import logging


log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='mylog-rest.json', filemode='a', format=log_format, level=logging.INFO)

# logging.warning('warn message')
# logging.info('info message')
# logging.debug('debug message')
# logging.error('error message')
# logging.critical('critical message')


class Client(object):

    def __init__(self, api_key, api_seceret_key, passphrase, use_server_time=False):

        self.API_KEY = api_key
        self.API_SECRET_KEY = api_seceret_key
        self.PASSPHRASE = passphrase
        self.use_server_time = use_server_time

    def _request(self, method, request_path, params, cursor=False):

        if method == c.GET:
            request_path = request_path + utils.parse_params_to_str(params)
        # url
        url = c.API_URL + request_path

        timestamp = utils.get_timestamp()
        # print(timestamp)
        # sign & header
        if self.use_server_time:
            timestamp = self._get_timestamp()
        # print(timestamp)

        body = json.dumps(params) if method == c.POST else ""

        sign = utils.sign(utils.pre_hash(timestamp, method, request_path, str(body)), self.API_SECRET_KEY)
        # print(utils.pre_hash(timestamp, method, request_path, str(body)))
        header = utils.get_header(self.API_KEY, sign, timestamp, self.PASSPHRASE)
        # send request
        response = None

        # print("url:", url)
        logging.info("url:" + url)
        # print("headers:", header)
        # print("body:", body)
        logging.info("body:" + body)
        try:
            if method == c.GET:
                response = requests.get(url, headers=header, timeout=(3, 3))
            elif method == c.POST:
                response = requests.post(url, data=body, headers=header, timeout=(3, 3))
                #response = requests.post(url, json=body, headers=header)
            elif method == c.DELETE:
                response = requests.delete(url, headers=header, timeout=(3, 3))

        except requests.exceptions.SSLError as rse:
            # 请求错误
            # print(rse)
            # print('requests.exceptions.SSLError')
            # exit()
            return None
        except requests.exceptions.ConnectionError as rce:
            # 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。
            # print(rce)
            # print('requests.exceptions.ConnectionError')
            # exit()
            return None
        except requests.exceptions.ReadTimeout as rto:
            # 读请求超时
            # print(rto)
            # print('requests.exceptions.ReadTimeout')
            # exit()
            return None
        except requests.exceptions.ConnectTimeout as cto:
            # 连接请求超时
            # print(cto)
            # print('requests.exceptions.ConnectTimeout')
            # exit()
            return None
        except exceptions.OkexAPIException as oae:
            # print(oae)
            # print('OkexAPIException')
            # exit()
            return None

        # exception handle
        if not str(response.status_code).startswith('2'):
            raise exceptions.OkexAPIException(response)
        try:
            res_header = response.headers
            if cursor:
                r = dict()
                try:
                    r['before'] = res_header['OK-BEFORE']
                    r['after'] = res_header['OK-AFTER']
                except:
                    # print("")
                    pass
                return response.json(), r
            else:
                return response.json()
        except ValueError:
            raise exceptions.OkexRequestException('Invalid Response: %s' % response.text)

    def _request_without_params(self, method, request_path):
        return self._request(method, request_path, {})

    def _request_with_params(self, method, request_path, params, cursor=False):
        return self._request(method, request_path, params, cursor)

    def _get_timestamp(self):
        url = c.API_URL + c.SERVER_TIMESTAMP_URL
        try:
            response = requests.get(url, timeout=(3, 3))

        except requests.exceptions.SSLError as rse:
            return None
        except requests.exceptions.ConnectionError as rce:
            return None
        except requests.exceptions.ReadTimeout as rto:
            return None
        except requests.exceptions.ConnectTimeout as cto:
            return None
        except exceptions.OkexAPIException as oae:
            return None

        if response.status_code == 200:
            return response.json()['iso']
        else:
            return ""




