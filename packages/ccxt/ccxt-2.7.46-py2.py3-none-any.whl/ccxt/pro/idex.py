# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.pro.base.exchange import Exchange
import ccxt.async_support
from ccxt.pro.base.cache import ArrayCache, ArrayCacheBySymbolById, ArrayCacheByTimestamp
from ccxt.base.errors import InvalidNonce


class idex(Exchange, ccxt.async_support.idex):

    def describe(self):
        return self.deep_extend(super(idex, self).describe(), {
            'has': {
                'ws': True,
                'watchOrderBook': True,
                'watchTrades': True,
                'watchOHLCV': True,
                'watchTicker': True,
                'watchTickers': False,  # for now
                'watchOrders': True,
                'watchTransactions': True,
            },
            'urls': {
                'test': {
                    'ws': 'wss://websocket-matic.idex.io/v1',
                },
                'api': {},
            },
            'options': {
                'tradesLimit': 1000,
                'ordersLimit': 1000,
                'OHLCVLimit': 1000,
                'watchOrderBookLimit': 1000,  # default limit
                'orderBookSubscriptions': {},
                'token': None,
                'fetchOrderBookSnapshotMaxAttempts': 10,
                'fetchOrderBookSnapshotMaxDelay': 10000,  # raise if there are no orders in 10 seconds
            },
        })

    async def subscribe(self, subscribeObject, messageHash, subscription=True):
        url = self.urls['test']['ws']
        request = {
            'method': 'subscribe',
            'subscriptions': [
                subscribeObject,
            ],
        }
        return await self.watch(url, messageHash, request, messageHash, subscription)

    async def subscribe_private(self, subscribeObject, messageHash):
        token = await self.authenticate()
        url = self.urls['test']['ws']
        request = {
            'method': 'subscribe',
            'token': token,
            'subscriptions': [
                subscribeObject,
            ],
        }
        return await self.watch(url, messageHash, request, messageHash)

    async def watch_ticker(self, symbol, params={}):
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the idex api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        name = 'tickers'
        subscribeObject = {
            'name': name,
            'markets': [market['id']],
        }
        messageHash = name + ':' + market['id']
        return await self.subscribe(self.extend(subscribeObject, params), messageHash)

    def handle_ticker(self, client, message):
        # {type: 'tickers',
        #   data:
        #    {m: 'DIL-ETH',
        #      t: 1599213946045,
        #      o: '0.09699020',
        #      h: '0.10301548',
        #      l: '0.09577222',
        #      c: '0.09907311',
        #      Q: '1.32723120',
        #      v: '297.80667468',
        #      q: '29.52142669',
        #      P: '2.14',
        #      n: 197,
        #      a: '0.09912245',
        #      b: '0.09686980',
        #      u: 5870}}
        type = self.safe_string(message, 'type')
        data = self.safe_value(message, 'data')
        marketId = self.safe_string(data, 'm')
        symbol = self.safe_symbol(marketId)
        messageHash = type + ':' + marketId
        timestamp = self.safe_integer(data, 't')
        close = self.safe_float(data, 'c')
        percentage = self.safe_float(data, 'P')
        change = None
        if (percentage is not None) and (close is not None):
            change = close * percentage
        ticker = {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(data, 'h'),
            'low': self.safe_float(data, 'l'),
            'bid': self.safe_float(data, 'b'),
            'bidVolume': None,
            'ask': self.safe_float(data, 'a'),
            'askVolume': None,
            'vwap': None,
            'open': self.safe_float(data, 'o'),
            'close': close,
            'last': close,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': None,
            'baseVolume': self.safe_float(data, 'v'),
            'quoteVolume': self.safe_float(data, 'q'),
            'info': message,
        }
        client.resolve(ticker, messageHash)

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the idex api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        name = 'trades'
        subscribeObject = {
            'name': name,
            'markets': [market['id']],
        }
        messageHash = name + ':' + market['id']
        trades = await self.subscribe(subscribeObject, messageHash)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trade(self, client, message):
        type = self.safe_string(message, 'type')
        data = self.safe_value(message, 'data')
        marketId = self.safe_string(data, 'm')
        messageHash = type + ':' + marketId
        trade = self.parse_ws_trade(data)
        keys = list(self.trades.keys())
        length = len(keys)
        if length == 0:
            limit = self.safe_integer(self.options, 'tradesLimit')
            self.trades = ArrayCacheBySymbolById(limit)
        trades = self.trades
        trades.append(trade)
        client.resolve(trades, messageHash)

    def parse_ws_trade(self, trade):
        # public trades
        # {m: 'DIL-ETH',
        #   i: '897ecae6-4b75-368a-ac00-be555e6ad65f',
        #   p: '0.09696995',
        #   q: '2.00000000',
        #   Q: '0.19393990',
        #   t: 1599504616247,
        #   s: 'buy',
        #   u: 6620}
        # private trades
        # {i: 'ee253d78-88be-37ed-a61c-a36395c2ce48',
        #   p: '0.09925382',
        #   q: '0.15000000',
        #   Q: '0.01488807',
        #   t: 1599499129369,
        #   s: 'sell',
        #   u: 6603,
        #   f: '0.00030000',
        #   a: 'DIL',
        #   g: '0.00856110',
        #   l: 'maker',
        #   S: 'pending'}
        marketId = self.safe_string(trade, 'm')
        symbol = self.safe_symbol(marketId)
        id = self.safe_string(trade, 'i')
        price = self.safe_float(trade, 'p')
        amount = self.safe_float(trade, 'q')
        cost = self.safe_float(trade, 'Q')
        timestamp = self.safe_integer(trade, 't')
        side = self.safe_string(trade, 's')
        fee = {
            'currency': self.safe_string(trade, 'a'),
            'cost': self.safe_float(trade, 'f'),
        }
        takerOrMarker = self.safe_string(trade, 'l')
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': None,
            'type': None,
            'takerOrMaker': takerOrMarker,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    async def watch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        """
        watches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int|None since: timestamp in ms of the earliest candle to fetch
        :param int|None limit: the maximum amount of candles to fetch
        :param dict params: extra parameters specific to the idex api endpoint
        :returns [[int]]: A list of candles ordered as timestamp, open, high, low, close, volume
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        name = 'candles'
        interval = self.safe_string(self.timeframes, timeframe, timeframe)
        subscribeObject = {
            'name': name,
            'markets': [market['id']],
            'interval': interval,
        }
        messageHash = name + ':' + market['id']
        ohlcv = await self.subscribe(subscribeObject, messageHash)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client, message):
        # {type: 'candles',
        #   data:
        #    {m: 'DIL-ETH',
        #      t: 1599477340109,
        #      i: '1m',
        #      s: 1599477300000,
        #      e: 1599477360000,
        #      o: '0.09911040',
        #      h: '0.09911040',
        #      l: '0.09911040',
        #      c: '0.09911040',
        #      v: '0.15000000',
        #      n: 1,
        #      u: 6531}}
        type = self.safe_string(message, 'type')
        data = self.safe_value(message, 'data')
        marketId = self.safe_string(data, 'm')
        messageHash = type + ':' + marketId
        parsed = [
            self.safe_integer(data, 's'),
            self.safe_float(data, 'o'),
            self.safe_float(data, 'h'),
            self.safe_float(data, 'l'),
            self.safe_float(data, 'c'),
            self.safe_float(data, 'v'),
        ]
        symbol = self.safe_symbol(marketId)
        interval = self.safe_string(data, 'i')
        timeframe = self.find_timeframe(interval)
        # TODO: move to base class
        self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
        stored = self.safe_value(self.ohlcvs[symbol], timeframe)
        if stored is None:
            limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
            stored = ArrayCacheByTimestamp(limit)
            self.ohlcvs[symbol][timeframe] = stored
        stored.append(parsed)
        client.resolve(stored, messageHash)

    def handle_subscribe_message(self, client, message):
        # {
        #   "type": "subscriptions",
        #   "subscriptions": [
        #     {
        #       "name": "l2orderbook",
        #       "markets": [
        #         "DIL-ETH"
        #       ]
        #     }
        #   ]
        # }
        subscriptions = self.safe_value(message, 'subscriptions')
        for i in range(0, len(subscriptions)):
            subscription = subscriptions[i]
            name = self.safe_string(subscription, 'name')
            if name == 'l2orderbook':
                markets = self.safe_value(subscription, 'markets')
                for j in range(0, len(markets)):
                    marketId = markets[j]
                    orderBookSubscriptions = self.safe_value(self.options, 'orderBookSubscriptions', {})
                    if not (marketId in orderBookSubscriptions):
                        symbol = self.safe_symbol(marketId)
                        if not (symbol in self.orderbooks):
                            orderbook = self.counted_order_book({})
                            orderbook.cache = []
                            self.orderbooks[symbol] = orderbook
                        self.spawn(self.fetch_order_book_snapshot, client, symbol)
                break

    async def fetch_order_book_snapshot(self, client, symbol, params={}):
        orderbook = self.orderbooks[symbol]
        market = self.market(symbol)
        messageHash = 'l2orderbook' + ':' + market['id']
        subscription = client.subscriptions[messageHash]
        if not subscription['fetchingOrderBookSnapshot']:
            subscription['startTime'] = self.milliseconds()
        subscription['fetchingOrderBookSnapshot'] = True
        maxAttempts = self.safe_integer(self.options, 'fetchOrderBookSnapshotMaxAttempts', 10)
        maxDelay = self.safe_integer(self.options, 'fetchOrderBookSnapshotMaxDelay', 10000)
        try:
            limit = self.safe_integer(subscription, 'limit', 0)
            # 3. Request a level-2 order book snapshot for the market from the REST API Order Books endpoint with limit set to 0.
            snapshot = await self.fetch_order_book(symbol, limit)
            firstBuffered = self.safe_value(orderbook.cache, 0)
            firstData = self.safe_value(firstBuffered, 'data')
            firstNonce = self.safe_integer(firstData, 'u')
            length = len(orderbook.cache)
            lastBuffered = self.safe_value(orderbook.cache, length - 1)
            lastData = self.safe_value(lastBuffered, 'data')
            lastNonce = self.safe_integer(lastData, 'u')
            bothExist = (firstNonce is not None) and (lastNonce is not None)
            # ensure the snapshot is inside the range of our cached messages
            # for example if the snapshot nonce is 100
            # the first nonce must be less than or equal to 101 and the last nonce must be greater than 101
            if bothExist and (firstNonce <= snapshot['nonce'] + 1) and (lastNonce > snapshot['nonce']):
                orderbook.reset(snapshot)
                for i in range(0, len(orderbook.cache)):
                    message = orderbook.cache[i]
                    data = self.safe_value(message, 'data')
                    u = self.safe_integer(data, 'u')
                    if u > orderbook['nonce']:
                        # 5. Discard all order book update messages with sequence numbers less than or equal to the snapshot sequence number.
                        # 6. Apply the remaining buffered order book update messages and any incoming order book update messages to the order book snapshot.
                        self.handle_order_book_message(client, message, orderbook)
                subscription['fetchingOrderBookSnapshot'] = False
                client.resolve(orderbook, messageHash)
            else:
                # 4. If the sequence in the order book snapshot is less than the sequence of the
                #    first buffered order book update message, discard the order book snapshot and retry step 3.
                # self will continue to recurse until we have a buffered message
                # since updates the order book endpoint depend on order events
                # so it will eventually raise if there are no orders on a pair
                subscription['numAttempts'] = subscription['numAttempts'] + 1
                timeElapsed = self.milliseconds() - subscription['startTime']
                maxAttemptsValid = subscription['numAttempts'] < maxAttempts
                timeElapsedValid = timeElapsed < maxDelay
                if maxAttemptsValid and timeElapsedValid:
                    self.delay(self.rateLimit, self.fetch_order_book_snapshot, client, symbol)
                else:
                    endpart = ' in ' + str(maxAttempts) + ' attempts' if (not maxAttemptsValid) else ' after ' + str(maxDelay) + ' milliseconds'
                    raise InvalidNonce(self.id + ' failed to synchronize WebSocket feed with the snapshot for symbol ' + symbol + endpart)
        except Exception as e:
            subscription['fetchingOrderBookSnapshot'] = False
            client.reject(e, messageHash)

    async def watch_order_book(self, symbol, limit=None, params={}):
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the idex api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        name = 'l2orderbook'
        subscribeObject = {
            'name': name,
            'markets': [market['id']],
        }
        messageHash = name + ':' + market['id']
        subscription = {
            'fetchingOrderBookSnapshot': False,
            'numAttempts': 0,
            'startTime': None,
        }
        if limit is None:
            subscription['limit'] = 1000
        else:
            subscription['limit'] = limit
        # 1. Connect to the WebSocket API endpoint and subscribe to the L2 Order Book for the target market.
        orderbook = await self.subscribe(subscribeObject, messageHash, subscription)
        return orderbook.limit()

    def handle_order_book(self, client, message):
        data = self.safe_value(message, 'data')
        marketId = self.safe_string(data, 'm')
        symbol = self.safe_symbol(marketId)
        orderbook = self.orderbooks[symbol]
        if orderbook['nonce'] is None:
            # 2. Buffer the incoming order book update subscription messages.
            orderbook.cache.append(message)
        else:
            self.handle_order_book_message(client, message, orderbook)

    def handle_order_book_message(self, client, message, orderbook):
        # {
        #   "type": "l2orderbook",
        #   "data": {
        #     "m": "DIL-ETH",
        #     "t": 1600197205037,
        #     "u": 94116643,
        #     "b": [
        #       [
        #         "0.09662187",
        #         "0.00000000",
        #         0
        #       ]
        #     ],
        #     "a": []
        #   }
        # }
        type = self.safe_string(message, 'type')
        data = self.safe_value(message, 'data')
        marketId = self.safe_string(data, 'm')
        messageHash = type + ':' + marketId
        nonce = self.safe_integer(data, 'u')
        timestamp = self.safe_integer(data, 't')
        bids = self.safe_value(data, 'b')
        asks = self.safe_value(data, 'a')
        self.handle_deltas(orderbook['bids'], bids)
        self.handle_deltas(orderbook['asks'], asks)
        orderbook['nonce'] = nonce
        orderbook['timestamp'] = timestamp
        orderbook['datetime'] = self.iso8601(timestamp)
        client.resolve(orderbook, messageHash)

    def handle_delta(self, bookside, delta):
        price = self.safe_float(delta, 0)
        amount = self.safe_float(delta, 1)
        count = self.safe_integer(delta, 2)
        bookside.store(price, amount, count)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    async def authenticate(self, params={}):
        time = self.seconds()
        lastAuthenticatedTime = self.safe_integer(self.options, 'lastAuthenticatedTime', 0)
        if time - lastAuthenticatedTime > 900:
            request = {
                'wallet': self.walletAddress,
                'nonce': self.uuidv1(),
            }
            response = await self.privateGetWsToken(self.extend(request, params))
            self.options['lastAuthenticatedTime'] = time
            self.options['token'] = self.safe_string(response, 'token')
        return self.options['token']

    async def watch_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        watches information on multiple orders made by the user
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the idex api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        await self.load_markets()
        name = 'orders'
        subscribeObject = {
            'name': name,
        }
        messageHash = name
        if symbol is not None:
            symbol = self.symbol(symbol)
            marketId = self.market_id(symbol)
            subscribeObject['markets'] = [marketId]
            messageHash = name + ':' + marketId
        orders = await self.subscribe_private(subscribeObject, messageHash)
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_since_limit(orders, since, limit, 'timestamp', True)

    def handle_order(self, client, message):
        # {
        #   "type": "orders",
        #   "data": {
        #     "m": "DIL-ETH",
        #     "i": "8f75dd30-f12d-11ea-b63c-df3381b4b5b4",
        #     "w": "0x0AB991497116f7F5532a4c2f4f7B1784488628e1",
        #     "t": 1599498857138,
        #     "T": 1599498857092,
        #     "x": "fill",
        #     "X": "filled",
        #     "u": 67695627,
        #     "o": "limit",
        #     "S": "buy",
        #     "q": "0.15000000",
        #     "z": "0.15000000",
        #     "Z": "0.01486286",
        #     "v": "0.09908573",
        #     "p": "1.00000000",
        #     "f": "gtc",
        #     "V": "2",
        #     "F": [
        #       {
        #         "i": "5cdc6d14-bc35-3279-ab5e-40d654ca1523",
        #         "p": "0.09908577",
        #         "q": "0.15000000",
        #         "Q": "0.01486286",
        #         "t": 1599498857092,
        #         "s": "sell",
        #         "u": 6600,
        #         "f": "0.00030000",
        #         "a": "DIL",
        #         "g": "0.00856977",
        #         "l": "maker",
        #         "S": "pending"
        #       }
        #     ]
        #   }
        # }
        type = self.safe_string(message, 'type')
        order = self.safe_value(message, 'data')
        marketId = self.safe_string(order, 'm')
        symbol = self.safe_symbol(marketId)
        timestamp = self.safe_integer(order, 't')
        fills = self.safe_value(order, 'F')
        trades = []
        for i in range(0, len(fills)):
            trades.append(self.parse_ws_trade(fills[i]))
        id = self.safe_string(order, 'i')
        side = self.safe_string(order, 's')
        orderType = self.safe_string(order, 'o')
        amount = self.safe_float(order, 'q')
        filled = self.safe_float(order, 'z')
        remaining = None
        if (amount is not None) and (filled is not None):
            remaining = amount - filled
        average = self.safe_float(order, 'v')
        price = self.safe_float(order, 'price', average)  # for market orders
        cost = None
        if (amount is not None) and (price is not None):
            cost = amount * price
        rawStatus = self.safe_string(order, 'X')
        status = self.parse_order_status(rawStatus)
        fee = {
            'currency': None,
            'cost': None,
        }
        lastTrade = None
        for i in range(0, len(trades)):
            lastTrade = trades[i]
            fee['currency'] = lastTrade['fee']['currency']
            fee['cost'] = self.sum(fee['cost'], lastTrade['fee']['cost'])
        lastTradeTimestamp = self.safe_integer(lastTrade, 'timestamp')
        parsedOrder = {
            'info': message,
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': orderType,
            'side': side,
            'price': price,
            'stopPrice': None,
            'triggerPrice': None,
            'amount': amount,
            'cost': cost,
            'average': average,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
            'trades': trades,
        }
        if self.orders is None:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            self.orders = ArrayCacheBySymbolById(limit)
        orders = self.orders
        orders.append(parsedOrder)
        symbolSpecificMessageHash = type + ':' + marketId
        client.resolve(orders, symbolSpecificMessageHash)
        client.resolve(orders, type)

    async def watch_transactions(self, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        name = 'balances'
        subscribeObject = {
            'name': name,
        }
        messageHash = name
        if code is not None:
            messageHash = name + ':' + code
        transactions = await self.subscribe_private(subscribeObject, messageHash)
        if self.newUpdates:
            limit = transactions.getLimit(code, limit)
        return self.filter_by_since_limit(transactions, since, limit, 'timestamp', True)

    def handle_transaction(self, client, message):
        # Update Speed: Real time, updates on any deposit or withdrawal of the wallet
        # {type: 'balances',
        #   data:
        #    {w: '0x0AB991497116f7F5532a4c2f4f7B1784488628e1',
        #      a: 'ETH',
        #      q: '0.11198667',
        #      f: '0.11198667',
        #      l: '0.00000000',
        #      d: '0.00'}}
        type = self.safe_string(message, 'type')
        data = self.safe_value(message, 'data')
        currencyId = self.safe_string(data, 'a')
        messageHash = type + ':' + currencyId
        code = self.safe_currency_code(currencyId)
        address = self.safe_string(data, 'w')
        transaction = {
            'info': message,
            'id': None,
            'currency': code,
            'amount': None,
            'address': address,
            'addressTo': None,
            'addressFrom': None,
            'tag': None,
            'tagTo': None,
            'tagFrom': None,
            'status': 'ok',
            'type': None,
            'updated': None,
            'txid': None,
            'timestamp': None,
            'datetime': None,
            'fee': None,
        }
        if not (code in self.transactions):
            limit = self.safe_integer(self.options, 'transactionsLimit', 1000)
            self.transactions[code] = ArrayCache(limit)
        transactions = self.transactions[code]
        transactions.append(transaction)
        client.resolve(transactions, messageHash)
        client.resolve(transactions, type)

    def handle_message(self, client, message):
        type = self.safe_string(message, 'type')
        methods = {
            'tickers': self.handle_ticker,
            'trades': self.handle_trade,
            'subscriptions': self.handle_subscribe_message,
            'candles': self.handle_ohlcv,
            'l2orderbook': self.handle_order_book,
            'balances': self.handle_transaction,
            'orders': self.handle_order,
        }
        if type in methods:
            method = methods[type]
            method(client, message)
