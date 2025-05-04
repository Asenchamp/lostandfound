from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


# Register your models here.

class customUserAdmin(UserAdmin):
    model = models.customUser
    filter_horizontal = ()

    list_display = ('username','email','last_name','first_name','phone_number','location')
    list_filter = ('location',)
    search_fields = ('username','email','location','phone_number')

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'phone_number', 'first_name', 'last_name', 'location')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
        # ('Account Status', {
        #     'fields': ('account_status','verified')
        # }),
    )

    def get_readonly_fields(self, request, obj = ...):
        
        #gets all of the field names defined in the model and make them readonly
        readonly = [field.name for field in self.model._meta.fields]
        return readonly
    

class authorityAdmin(admin.ModelAdmin):
    list_display = ('user','user__email','user__phone_number','user__location','authority_type')
    search_fields = ('user','user__email','user__location','user__phone_number')
    list_filter = ('authority_type','user__location',)

admin.site.register(models.customUser,customUserAdmin)
admin.site.register(models.authority_type)
admin.site.register(models.authority, authorityAdmin)

