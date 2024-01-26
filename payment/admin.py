from django.contrib import admin
from.models import *
# Register your models here.


class WalletAdmin(admin.ModelAdmin):
    readonly_fields =('wallet','owner','password',)

admin.site.register(Pay)
admin.site.register(Order)
admin.site.register(Wallet,WalletAdmin)