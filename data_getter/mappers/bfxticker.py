from .common import Getter
from data_getter.schemas.bfx import BFXTickerTradingModel, BFXTickerFundingModel
from data_getter.celery import app as celery_app


# @celery_app.task(bind=True)
class BFXTickerGetter(Getter):
    url = "https://api-pub.bitfinex.com/v2/tickers?symbols=ALL"

    def map(self):
        return map(lambda pair: BFXTickerTradingModel(pair) if pair[0][0] == "t" else BFXTickerFundingModel(pair),
                   self.response)

        # for pair in self.response:
        #     if pair[0][0] == "t":
        #         return BFXTickerTradingModel(pair)
        #     elif pair[0][0] == "f":
        #         return BFXTickerFundingModel(pair)

        # BFXTickerTradingModel(symbol=pair[0][0],
        #                                        bid=,
        #                                        bid_size=,
        #                                        ask=,
        #                                        ask_size=,
        #                                        daily_change,
        #                                        daily_change_relative,
        #                                        last_price,
        #                                        volume,
        #                                        high,
        #                                        low,
        #                                        )
