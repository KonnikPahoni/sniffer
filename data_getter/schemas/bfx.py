from django.db import models


class BFXTickerTradingModel(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, unique=True, db_index=True)
    symbol = models.CharField(max_length=255)
    bid = models.FloatField(null=True, blank=True)
    bid_size = models.FloatField(null=True, blank=True)
    ask = models.FloatField(null=True, blank=True)
    ask_size = models.FloatField(null=True, blank=True)
    daily_change = models.FloatField(null=True, blank=True)
    daily_change_relative = models.FloatField(null=True, blank=True)
    last_price = models.FloatField(null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    high = models.FloatField(null=True, blank=True)
    low = models.FloatField(null=True, blank=True)


class BFXTickerFundingModel(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, unique=True, db_index=True)
    symbol = models.CharField(max_length=255)
    frr = models.FloatField(null=True, blank=True)
    bid = models.FloatField(null=True, blank=True)
    bid_period = models.FloatField(null=True, blank=True)
    bid_size = models.FloatField(null=True, blank=True)
    ask = models.FloatField(null=True, blank=True)
    ask_period = models.FloatField(null=True, blank=True)
    ask_size = models.FloatField(null=True, blank=True)
    daily_change = models.FloatField(null=True, blank=True)
    daily_change_relative = models.FloatField(null=True, blank=True)
    last_price = models.FloatField(null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    high = models.FloatField(null=True, blank=True)
    low = models.FloatField(null=True, blank=True)
    frr_amount_available = models.FloatField(null=True, blank=True)
