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
            'fields': ('Review', 'GetReview')
        }),
    )
    list_display = ('User', 'Name', 'Status')
    readonly_fields = ('GetReview', 'TimeStamp', 'LastMotified')

admin.site.register(group)
admin.site.register(profile, ProfileAdmin)
admin.site.register(checkcode)
admin.site.register(country)
