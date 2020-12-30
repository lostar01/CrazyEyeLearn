from django.contrib import admin
from web import models
from web import auth_admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class HostGroupsAdmin(admin.ModelAdmin):
    fields = ('name','bind_hosts','memo')

    filter_horizontal = ('bind_hosts',)

admin.site.register(models.IDC)
admin.site.register(models.Host)
admin.site.register(models.RemoteUser)
admin.site.register(models.BindHost)
# admin.site.register(models.UserProfile)
admin.site.register(models.HostGroups,HostGroupsAdmin)
admin.site.register(models.SessionRecord)