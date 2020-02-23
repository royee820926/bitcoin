# encoding=utf-8


class ApiBase:
    # _api_key = '8604b6c5-36aa-4281-99cd-e61083211cfd'
    # _secret_key = 'D999D1697CC299F8140E85E0E24156D9'
    _api_key = '948d9215-8092-463e-b965-6561c861d105'
    _secret_key = '1740A3D0CCBEA6272DCF402C0428342F'
    _passphrase = 'djxp19820926'

    # 现货交易api实例
    _spot_api = None

    # 合约交易api实例
    _swap_api = None

    # 资金账户
    _account_api = None

    # 公共-获取指数成分
    _index_api = None
