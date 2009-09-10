from django.contrib import admin

import models

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email',)
    
admin.site.register(models.Invitation, InvitationAdmin)
