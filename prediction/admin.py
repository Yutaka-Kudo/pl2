from django.contrib import admin
from .models import PRED_data, STORE_data, CUSTOMER_data


class PRED_dataAdmin(admin.ModelAdmin):
    list_display = ["date", "week", "holiday", "shorttime_at20", "peopleflow_shibuya", "corona_tokyo", "rain_l", "rain_d", "tempe_l", "tempe_d"]


admin.site.register(PRED_data, PRED_dataAdmin)


class STORE_dataAdmin(admin.ModelAdmin):
    list_display = ["store_name", "id"]


admin.site.register(STORE_data, STORE_dataAdmin)


class CUSTOMER_dataAdmin(admin.ModelAdmin):
    list_display = ["date", "week", "store", "cust_l", "cust_d", "price_l", "price_d", "id"]


admin.site.register(CUSTOMER_data, CUSTOMER_dataAdmin)
