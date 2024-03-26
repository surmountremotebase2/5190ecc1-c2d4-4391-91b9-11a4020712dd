from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the SPDR sector ETFs to use in the strategy
        self.tickers = [
            "XLB",  # Materials
            "XLE",  # Energy
            "XLF",  # Financials
            "XLI",  # Industrials
            "XLK",  # Technology
            "XLP",  # Consumer Staples
            "XLRE", # Real Estate
            "XLU",  # Utilities
            "XLV",  # Health Care
            "XLY"   # Consumer Discretionary
        ]

    @property
    def interval(self):
        # Use daily data for the strategy
        return "1day"

    @property
    def assets(self):
        # Return the list of tickers to be used
        return self.tickers

    def run(self, data):
        # Initialize an empty dictionary to store momentum for each ETF
        momentum_scores = {}

        # Calculate the 90-day momentum for each ETF and store it
        for ticker in self.tickers:
            momentum = MACD(ticker, data["ohlcv"], 20, 50)
            if momentum:
                momentum_scores[ticker] = momentum[-1]  # Use the most recent momentum value

        # Sort the ETFs by their momentum scores in descending order
        sorted_tickers = sorted(momentum_scores, key=momentum_scores.get, reverse=True)

        allocation_dict = {}
        
        # Assign positive allocations to the top 3 ETFs based on momentum
        for ticker in sorted_tickers[:3]:
            allocation_dict[ticker] = 1 / len(sorted_tickers[:3])  # Evenly divide capital among top 3

        # Assign negative allocations (short positions) to the bottom 3 ETFs based on momentum
        for ticker in sorted_tickers[-3:]:
            allocation_dict[ticker] = -1 / len(sorted_tickers[-3:])  # Evenly divide capital among bottom 3

        # Return the TargetAllocation object with our calculated allocations
        return TargetAllocation(allocation_dict)