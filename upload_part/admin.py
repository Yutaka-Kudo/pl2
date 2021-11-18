from django.contrib import admin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin


from upload_part.models import PL_data, FoodCosts, DrinkCosts, LaborCosts, UtilityCosts_ComunicationCosts, AdvertisingCosts, OtherCosts, TaxExemptExpenses


class PL_dataAdmin(admin.ModelAdmin):
    list_display = ["y_m", "category", "amountSold"]


admin.site.register(PL_data, PL_dataAdmin)


class FoodCostsAdmin(admin.ModelAdmin):
    list_display = ["pl_data"]


admin.site.register(FoodCosts, FoodCostsAdmin)


class DrinkCostsAdmin(admin.ModelAdmin):
    list_display = ["pl_data"]


admin.site.register(DrinkCosts, DrinkCostsAdmin)


class LaborCostsAdmin(admin.ModelAdmin):
    list_display = ["pl_data"]


admin.site.register(LaborCosts, LaborCostsAdmin)


class UtilityCosts_ComunicationCostsAdmin(admin.ModelAdmin):
    list_display = ["pl_data"]


admin.site.register(UtilityCosts_ComunicationCosts, UtilityCosts_ComunicationCostsAdmin)


class AdvertisingCostsAdmin(admin.ModelAdmin):
    list_display = ["pl_data"]


admin.site.register(AdvertisingCosts, AdvertisingCostsAdmin)


class OtherCostsAdmin(admin.ModelAdmin):
    list_display = ["pl_data"]


admin.site.register(OtherCosts, OtherCostsAdmin)


class TaxExemptExpensesAdmin(admin.ModelAdmin):
    list_display = ["pl_data"]


admin.site.register(TaxExemptExpenses, TaxExemptExpensesAdmin)

