from django.contrib import admin

# Register your models here.
from index.models import GoodsType, Goods



class GoodsAdmin(admin.ModelAdmin):
    list_filter = ('goodsType',)

admin.site.register(GoodsType)
admin.site.register(Goods,GoodsAdmin)















