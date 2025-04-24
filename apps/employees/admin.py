from django.contrib import admin

from .models import Employee, EmployeeSetting

# Register your models here.


@admin.register(EmployeeSetting)
class EmployeeSettingAdmin(admin.ModelAdmin):
    list_display = ("actor", "role")
    list_filter = ("actor",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "job_title", "site", "company")
    list_filter = ("full_name",)
