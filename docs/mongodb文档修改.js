// 数据库添加索引
db.getCollection('BCH-USDT').createIndex({'time': 1});
db.getCollection('BSV-USDT').createIndex({'time': 1});
db.getCollection('BTC-USDT').createIndex({'time': 1});
db.getCollection('EOS-USDT').createIndex({'time': 1});
db.getCollection('ETC-USDT').createIndex({'time': 1});
db.getCollection('ETH-USDT').createIndex({'time': 1});
db.getCollection('LTC-USDT').createIndex({'time': 1});
db.getCollection('TRX-USDT').createIndex({'time': 1});
db.getCollection('XRP-USDT').createIndex({'time': 1});

db.getCollection('BCH-USD-SWAP').createIndex({'time': 1});
db.getCollection('BSV-USD-SWAP').createIndex({'time': 1});
db.getCollection('BTC-USD-SWAP').createIndex({'time': 1});
db.getCollection('EOS-USD-SWAP').createIndex({'time': 1});
db.getCollection('ETC-USD-SWAP').createIndex({'time': 1});
db.getCollection('ETH-USD-SWAP').createIndex({'time': 1});
db.getCollection('LTC-USD-SWAP').createIndex({'time': 1});
db.getCollection('TRX-USD-SWAP').createIndex({'time': 1});
db.getCollection('XRP-USD-SWAP').createIndex({'time': 1});

// 数据库添加buy_volume和sell_volume字段，默认为0
db.getCollection('BCH-USDT').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('BSV-USDT').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('BTC-USDT').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('EOS-USDT').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('ETC-USDT').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('ETH-USDT').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('LTC-USDT').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('TRX-USDT').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('XRP-USDT').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});

db.getCollection('BCH-USD-SWAP').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('BSV-USD-SWAP').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('BTC-USD-SWAP').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('EOS-USD-SWAP').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('ETC-USD-SWAP').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('ETH-USD-SWAP').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('LTC-USD-SWAP').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('TRX-USD-SWAP').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
db.getCollection('XRP-USD-SWAP').update({}, {'$set': {'buy_volume': 0, 'sell_volume': 0}}, {'multi': true, 'upsert':  false});
