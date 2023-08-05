from okx_candle.market._base import MarketBase


class Ticker(MarketBase):

    # 获取所有产品的行情列表
    def get_bookTickers(self) -> dict:
        return self._marketAPI.get_tickers(instType=self.instType)

    # 获取所有产品的行情字典
    def get_bookTickersMap(self) -> dict:
        bookTickers_result = self.get_bookTickers()
        # [ERROR RETURN] 数据异常
        if bookTickers_result['code'] != '0':
            return bookTickers_result
        data_map = {}
        for ticker in bookTickers_result['data']:
            symbol = ticker['instId']
            data_map[symbol] = ticker

        bookTickers_result['data'] = data_map
        return bookTickers_result

    # 获取单个产品的行情
    def get_bookTicker(self, symbol: str) -> dict:
        return self._marketAPI.get_ticker(instId=symbol)

    # 产品深度
    def get_deepTicker(self, symbol: str, sz: int = 1):
        return self._marketAPI.get_books(instId=symbol, sz=sz)
