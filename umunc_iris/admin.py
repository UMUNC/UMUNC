from django.contrib import admin
from umunc_iris.models import *

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Status', {
            'fields': ('User', 'TimeStamp', 'LastMotified', 'Init', 'Status')
        }),
        ('Basic Information', {
            'fields': ('Name', 'Sex', 'Age', 'IDNum', 'School', 'Grade', 'GName', 'GPhone', 'Phone', 'Phone2', 'QQ', 'Wechat', 'MunAge', 'MunRsm', 'Commitee', 'Commitee2', 'Adjust')
        }),
        ('Group Information', {
			'classes': ('collapse'),
            'fields': ('Group', 'Leader')
        }),
        ('Distribution', {
			'classes': ('collapse'),
            'fields': ('Country', 'Identify')
        }),
        ('Review', {
			'classes': ('collapse'),
            'fields': ('Review', 'Comment')
        }),
    )
    list_display = ('User', 'Name','Status')

    readonly_fields = ('TimeStamp', 'LastMotified')
    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('profile.control_all'):
            return ('User', 'Name', 'Status')
        else:
            return ('User', 'Name', 'Status')

admin.site.register(group)
admin.site.register(profile, ProfileAdmin)
admin.site.register(checkcode)
admin.site.register(country)
