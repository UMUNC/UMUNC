#coding=utf-8
from django.contrib import admin
from umunc_iris.models import *
import django.utils.html.escape

class GroupAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic', {
            'fields': ('Name', 'School', 'Password')
        }),
        ('Status', {
            'fields': ('Paycode', 'Payment', 'Group')
        }),
        ('Interviewer', {
            'classes': ('collapse'),
            'fields': ('sendmail',)
        }),
    )
    list_display = ('User', 'Name','Status')

    readonly_fields = ('TimeStamp', 'LastMotified', 'sendmail')
    def sendmail(self, obj):
        return django.utils.html.escape(u'''
            <a href=\"/iris/admin/sendmail/?command=sendmail_payment&id='''+obj.id+u'''\">发送缴费确认邮件</a>
            ''')

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
        ('Interviewer', {
            'classes': ('collapse'),
            'fields': ('Interviewer','sendmail')
        }),
    )
    list_display = ('User', 'Name','Status')

    readonly_fields = ('TimeStamp', 'LastMotified', 'sendmail')
    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('profile.control_all'):
            return ('TimeStamp', 'LastMotified', 'sendmail')
        else:
            return ('TimeStamp', 'LastMotified', 'sendmail')
    def sendmail(self, obj):
        return django.utils.html.escape(u'''
            <a href=\"/iris/admin/sendmail/?command=sendmail_emailcheck&id='''+obj.User.id+u'''\">发送注册邮件</a><br/>
            <a href=\"/iris/admin/sendmail/?command=sendmail_interview&id='''+obj.User.id+u'''\">发送面试通知邮件</a><br/>
            <a href=\"/iris/admin/sendmail/?command=sendmail_identify&id='''+obj.User.id+u'''\">发送席位通知邮件</a><br/>
            <a href=\"/iris/admin/sendmail/?command=sendmail_payment_user&id='''+obj.User.id+u'''\">发送缴费确认邮件</a>
            ''')

admin.site.register(group, GroupAdmin)
admin.site.register(profile, ProfileAdmin)
admin.site.register(checkcode)
admin.site.register(country)
