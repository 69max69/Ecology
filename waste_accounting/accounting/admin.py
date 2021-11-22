from django.contrib import admin
from .models import *
# Register your models here.

class StaffAdmine(admin.ModelAdmin):
    list_display = ('user', 'branch', 'department', 'function')
    search_fields = ['user']
    list_filter = ('branch', 'department', 'function')

class NameOfBranchAdmine(admin.ModelAdmin):
    list_display = ['name', 'adress']
    search_fields = ['name']
    list_filter = ['name']

class NameOfObjectsAdmine(admin.ModelAdmin):
    list_display = ['name', 'branch', 'adress']
    search_fields = ['name' ]
    list_filter = ['branch']

class WasteAdmine(admin.ModelAdmin):
    list_display = ['name']

# class EducatedWasteAdmine(admin.ModelAdmin):
#     list_display = ['name', 'object_name', 'quantity', 'date_of_educated', 'user_name', 'created_at', 'updated_at',
#                     'branch']
#     list_filter = ['branch']
#     search_fields = ['object_name']

# class ReclaimedWasteAdmine(admin.ModelAdmin):
#     list_display = ['name', 'object_name', 'quantity', 'date_of_reclaimed', 'user_name', 'created_at', 'updated_at',
#                     'branch']
#     list_filter = ['branch']
#     search_fields = ['object_name']
#
# class TransferredWasteAdmine(admin.ModelAdmin):
#     list_display = ['name', 'object_name', 'quantity', 'date_of_transferred', 'user_name', 'created_at', 'updated_at',
#                     'branch']
#     list_filter = ['branch']
#     search_fields = ['object_name']


class TypeTransferrAdmine(admin.ModelAdmin):
    list_display = ['name']

class CounterpartiesAdmine(admin.ModelAdmin):
    list_display = ['name', 'date_of_contract', 'number_of_contract']


admin.site.register(Staff, StaffAdmine)
admin.site.register(NameOfBranch, NameOfBranchAdmine)
admin.site.register(NameOfObjects,NameOfObjectsAdmine)
admin.site.register(Waste, WasteAdmine)
# admin.site.register(EducatedWaste, EducatedWasteAdmine)
# admin.site.register(ReclaimedWaste, ReclaimedWasteAdmine)
# admin.site.register(TransferredWaste, TransferredWasteAdmine)
admin.site.register(TypeTransferr, TypeTransferrAdmine)
admin.site.register(Counterparties, CounterpartiesAdmine)
