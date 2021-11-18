from django.contrib import admin

# Register your models here.
from . import models


class ProgressAdmin(admin.ModelAdmin):
    list_display = ["now", "total"]


admin.site.register(models.Progress, ProgressAdmin)


class TargetFileNameAdmin(admin.ModelAdmin):
    list_display = ["store", "file_name"]


admin.site.register(models.TargetFileName, TargetFileNameAdmin)


class CostsAdmin(admin.ModelAdmin):
    list_display = ["store"]


admin.site.register(models.Costs, CostsAdmin)
