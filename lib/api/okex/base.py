# encoding=utf-8


class ApiBase:
    # at corp
    # ip: 114.95.120.190
    __api_key = '8774854b-819e-4ea3-a48d-f4fff762d249'
    __secret_key = 'E69D1D2119651B9D8F1B2C0A6E355E1B'

    # at home
    # __api_key = '948d9215-8092-463e-b965-6561c861d105'
    # __secret_key = '1740A3D0CCBEA6272DCF402C0428342F'

    __passphrase = 'djxp19820926'

    # 现货交易api实例
    _spot_api = None

    # 合约交易api实例
    _swap_api = None

    # 资金账户
    _account_api = None

    # 公共-获取指数成分
    _index_api = None

    @classmethod
    def get_api_key(cls):
        return cls.__api_key

    @classmethod
    def get_secret_key(cls):
        return cls.__secret_key

    @classmethod
    def get_passphrase(cls):
        return cls.__passphrase
