# Register your models here.
from django.contrib import admin

from website.models import Coin, CoinPrice, Rule

admin.site.register(Coin)
admin.site.register(CoinPrice)
admin.site.register(Rule)
