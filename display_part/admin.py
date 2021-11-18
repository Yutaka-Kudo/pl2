from django.contrib import admin

# Register your models here.

from . import models


class ManagersAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "c_d_permission"]


admin.site.register(models.Managers, ManagersAdmin)
