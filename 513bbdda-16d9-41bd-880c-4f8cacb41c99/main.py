from surmount.base_class import Strategy, TargetAllocation


class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ["AAPL", ...]
        self.data_list = [...]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list