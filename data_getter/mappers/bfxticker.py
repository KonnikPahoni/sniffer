from .common import Getter
from data_getter.schemas.bfx import BFXTickerTradingModel, BFXTickerFundingModel


class BFXTickerGetter(Getter):
    url = "https://api-pub.bitfinex.com/v2/tickers?symbols=ALL"

    def create_objects(self):
        objects = []
        for pair in self.response:
            objects.append(self.create_object(pair))
        self.objects = objects
        return self.objects

    @staticmethod
    def create_object(pair_):
        if pair_[0][0] == "t":
            return BFXTickerTradingModel(symbol=pair_[0],
                                         bid=pair_[1],
                                         bid_size=pair_[2],
                                         ask=pair_[3],
                                         ask_size=pair_[4],
                                         daily_change=pair_[5],
                                         daily_change_relative=pair_[6],
                                         last_price=pair_[7],
                                         volume=pair_[8],
                                         high=pair_[9],
                                         low=pair_[10],
                                         )
        elif pair_[0][0] == "f":
            return BFXTickerFundingModel(symbol=pair_[0],
                                         frr=pair_[1],
                                         bid=pair_[2],
                                         bid_period=pair_[3],
                                         bid_size=pair_[4],
                                         ask=pair_[5],
                                         ask_period=pair_[6],
                                         ask_size=pair_[7],
                                         daily_change=pair_[8],
                                         daily_change_relative=pair_[9],
                                         last_price=pair_[10],
                                         volume=pair_[11],
                                         high=pair_[12],
                                         low=pair_[13],
                                         frr_amount_available=pair_[16]
                                         )
