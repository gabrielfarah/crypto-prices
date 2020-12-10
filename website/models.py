# Create your models here.
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Coin(models.Model):
    name = models.CharField(max_length=128,
                            help_text=_('The name of the coin'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CoinPrice(models.Model):
    coin = models.ForeignKey(Coin,
                             on_delete=models.CASCADE,
                             related_name='prices',
                             db_index=True)
    price = models.FloatField(null=True)

    def __str__(self):
        return self.coin.name


class Rule(models.Model):
    name = models.CharField(max_length=128,
                            help_text=_('The name of the rule'))
    owner = models.ForeignKey(get_user_model(),
                                 on_delete=models.CASCADE,
                                 related_name='rule',
                                 db_index=True)
    coin = models.ForeignKey(Coin,
                             on_delete=models.CASCADE,
                             related_name='rules',
                             db_index=True)
    logic = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
