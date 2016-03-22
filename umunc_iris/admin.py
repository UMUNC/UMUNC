#coding=utf-8
from django.contrib import admin
from django.template import Context, Template
from umunc_iris.models import *
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ExportMixin, ImportExportModelAdmin

class GroupResource(resources.ModelResource):
    class Meta:
        model = group
        fields = ('Name', 'School', 'Password', 'Paycode', 'Payment', 'Group')

class ProfileResource(resources.ModelResource):
    class Meta:
        model = profile

class GroupAdmin(ImportExportModelAdmin, ExportMixin):
    fieldsets = (
        ('Basic', {
            'fields': ('Name', 'School', 'Password')
        }),
        ('Status', {
            'fields': ('Paycode', 'Payment', 'Group')
        }),
        ('Mail', {
            'classes': ('collapse'),
            'fields': ('sendmail',)
        }),
        ('Member', {
            'classes': ('collapse'),
            'fields': ('member',)
        }),
    )
    list_display = ('Name', 'School', 'Paycode', 'Payment')

    readonly_fields = ('TimeStamp', 'LastMotified', 'sendmail')

    resource_class = GroupResource

    def sendmail(self, obj):
        return mark_safe(u'''
            <a target="_blank" href=\"/iris/admin/sendmail/?command=sendmail_payment&id='''+str(obj.id)+u'''\">发送缴费确认邮件</a>
            ''')
    def sendmail(self, obj):
        t = Template('''
            <table class="table table-striped table-hover table-bordered">
                <thead>
                    <th>用户名</th>
                    <th>姓名</th>
                    <th>状态</th>
                </thead>
                <tbody>
                    {% for u in group.profile_set.all %}
                        <tr class="
                            {% if u.Status > 5 %}success{% endif %}
                            {% if u.Status < 0 %}danger{% endif %}
                        ">
                            <td>{{u.User.username}}</td>
                            <td>{{u.Name}}</td>
                            <td>{{u.get_Status_display}}</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
            ''')
        c = Context({'group': obj})
        return mark_safe(t.render(c))

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
            'fields': ('Interviewer',)
        }),
        ('Mail', {
            'classes': ('collapse'),
            'fields': ('sendmail',)
        }),
    )
    list_display = ('User', 'Name', 'Status', )

    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('profile.control_all'):
            return ('User', 'TimeStamp', 'LastMotified','sendmail')
        else:
            return ('User', 'TimeStamp', 'LastMotified', 'Init', 'Status', 'Name', 'Sex', 'Age', 'IDNum', 'School', 'Grade', 'GName', 'GPhone', 'Phone', 'Phone2', 'QQ', 'Wechat', 'MunAge', 'MunRsm', 'Commitee', 'Commitee2', 'Adjust', 'Group', 'Leader', 'Review','sendmail')
    def sendmail(self, obj):
        return mark_safe(u'''
            <a target="_blank" href=\"/iris/admin/sendmail/?command=sendmail_emailcheck&id='''+str(obj.User.id)+u'''\">发送注册邮件</a><br/>
            <a target="_blank" href=\"/iris/admin/sendmail/?command=sendmail_interview&id='''+str(obj.User.id)+u'''\">发送面试通知邮件</a><br/>
            <a target="_blank" href=\"/iris/admin/sendmail/?command=sendmail_identify&id='''+str(obj.User.id)+u'''\">发送席位通知邮件</a><br/>
            <a target="_blank" href=\"/iris/admin/sendmail/?command=sendmail_payment_user&id='''+str(obj.User.id)+u'''\">发送缴费确认邮件</a>
            ''')

admin.site.register(group, GroupAdmin)
admin.site.register(profile, ProfileAdmin)
admin.site.register(checkcode)
admin.site.register(country)

