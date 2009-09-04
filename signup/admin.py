from django.contrib import admin

import models

class ConstituencyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',),}

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'last_login')
    list_filter = ('constituencies','is_active')
    search_fields = ('first_name', 'last_name', 'email')

admin.site.register(models.Constituency, ConstituencyAdmin)
admin.site.register(models.CustomUser, UserAdmin)
