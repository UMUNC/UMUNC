#coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import User
from django.template import Context, Template
from umunc_iris.models import *
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from import_export import resources
from import_export.admin import ExportActionModelAdmin

class GroupResource(resources.ModelResource):
    class Meta:
        model = group
        fields = ('Name', 'School', 'Password', 'Paycode', 'Payment', 'Group')

class ProfileResource(resources.ModelResource):
    class Meta:
        model = profile

class GroupAdmin(ExportActionModelAdmin):
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

    readonly_fields = ('sendmail', 'member')

    resource_class = GroupResource

    actions_on_top = False
    actions_on_bottom = True

    def sendmail(self, obj):
        return mark_safe(u'''<a target="_blank" class="btn btn-sm btn-default" href=\"/iris/admin/sendmail/?command=sendmail_payment&id='''+str(obj.id)+u'''\">发送缴费确认邮件</a>
            ''')

    def member(self, obj):
        t = Template(u'''<table class="table table-striped table-hover table-bordered">\
                <thead>\
                    <th>用户名</th>\
                    <th>姓名</th>\
                    <th>状态</th>\
                </thead>\
                <tbody>\
                    {% for u in group.profile_set.all %}\
                        <tr class="\
                            {% if u.Status > 5 %}success{% endif %}\
                            {% if u.Status < 0 %}danger{% endif %}\
                        ">\
                            <td><a href="/admin/umunc_iris/profile/{{u.id}}/">{{u.User.username}}</td>\
                            <td>{{u.Name}}</td>\
                            <td>{{u.get_Status_display}}</td>\
                        </tr>\
                    {% endfor %}\
                </tbody>\
            </table>''')
        c = Context({'group': obj})
        return t.render(c)

    def export_admin_action(self, request, queryset):
        """
        Exports the selected rows using file_format.
        """
        if request.user.has_perm('umunc_iris.control_all'):
            return super.export_admin_action(request, queryset)
        else:
            return HttpResponse(u'<script>alert("无权下载");window.opener=null;window.close();</script>')

    actions = [export_admin_action]

class ProfileAdmin(ExportActionModelAdmin):
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
            'fields': ('System', 'Country', 'Identify')
        }),
        ('Review', {
			'classes': ('collapse'),
            'fields': ('Review1', 'Review2', 'Review3', 'Review4', 'Comment')
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

    list_display = ('User', 'Name', 'Status', 'Group', 'Commitee','System', 'Country', 'Identify',)

    search_fields = ('User__username', 'Name', 'School', 'Phone', 'Phone2',)

    list_filter = ('Status', 'Group', 'School', 'System', 'Country', 'Commitee', 'Commitee2',)

    resource_class = ProfileResource

    actions_on_top = False
    actions_on_bottom = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "Interviewer":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super(ProfileAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('umunc_iris.control_all'):
            return ('User', 'TimeStamp', 'LastMotified','sendmail')
        else:
            return ('User', 'TimeStamp', 'LastMotified', 'Init', 'Status', 'Name', 'Sex', 'Age', 'IDNum', 'School', 'Grade', 'GName', 'GPhone', 'Phone', 'Phone2', 'QQ', 'Wechat', 'MunAge', 'MunRsm', 'Commitee', 'Commitee2', 'Adjust', 'Group', 'Leader', 'Review1', 'Review2', 'Review3', 'Review4', 'sendmail')

    def sendmail(self, obj):
        return mark_safe(u'''<a target="_blank" class="btn btn-sm btn-default" href=\"/iris/admin/sendmail/?command=sendmail_emailcheck&id='''+str(obj.User.id)+u'''\">发送注册邮件</a><br/>
            <a target="_blank" class="btn btn-sm btn-default" href=\"/iris/admin/sendmail/?command=sendmail_interview&id='''+str(obj.User.id)+u'''\">发送面试通知邮件</a><br/>
            <a target="_blank" class="btn btn-sm btn-default" href=\"/iris/admin/sendmail/?command=sendmail_interview_reject&id='''+str(obj.User.id)+u'''\">发送面试重分配通知邮件</a><br/>
            <a target="_blank" class="btn btn-sm btn-default" href=\"/iris/admin/sendmail/?command=sendmail_identify&id='''+str(obj.User.id)+u'''\">发送席位通知邮件</a><br/>
            <a target="_blank" class="btn btn-sm btn-default" href=\"/iris/admin/sendmail/?command=sendmail_payment_user&id='''+str(obj.User.id)+u'''\">发送缴费确认邮件</a>
            ''')

class CountryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Status', {
            'fields': ('Name',)
        }),
        ('Member', {
            'classes': ('collapse'),
            'fields': ('member',)
        }),
    )

    readonly_fields = ('member',)

    list_display = ('Name',)

    def member(self, obj):
        t = Template(u'''<table class="table table-striped table-hover table-bordered">\
                <thead>\
                    <th>用户名</th>\
                    <th>姓名</th>\
                    <th>状态</th>\
                    <th>席位 所属体系</th>\
                    <th>席位 所属国家</th>\
                    <th>席位 席位名称</th>\
                </thead>\
                <tbody>\
                    {% for u in country.profile_set.all %}\
                        <tr class="\
                            {% if u.Status > 5 %}success{% endif %}\
                            {% if u.Status < 0 %}danger{% endif %}\
                        ">\
                            <td><a href="/admin/umunc_iris/profile/{{u.id}}/">{{u.User.username}}</td>\
                            <td>{{u.Name}}</td>\
                            <td>{{u.get_Status_display}}</td>\
                            <td>{{u.System}}</td>\
                            <td>{{u.Country}}</td>\
                            <td>{{u.Identify}}</td>\
                        </tr>\
                    {% endfor %}\
                </tbody>\
            </table>''')
        c = Context({'country': obj})
        return t.render(c)

class SystemAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Status', {
            'fields': ('Name',)
        }),
        ('Member', {
            'classes': ('collapse'),
            'fields': ('member',)
        }),
    )

    readonly_fields = ('member',)

    list_display = ('Name',)

    def member(self, obj):
        t = Template(u'''<table class="table table-striped table-hover table-bordered">\
                <thead>\
                    <th>用户名</th>\
                    <th>姓名</th>\
                    <th>状态</th>\
                    <th>席位 所属体系</th>\
                    <th>席位 所属国家</th>\
                    <th>席位 席位名称</th>\
                </thead>\
                <tbody>\
                    {% for u in country.profile_set.all %}\
                        <tr class="\
                            {% if u.Status > 5 %}success{% endif %}\
                            {% if u.Status < 0 %}danger{% endif %}\
                        ">\
                            <td><a href="/admin/umunc_iris/profile/{{u.id}}/">{{u.User.username}}</td>\
                            <td>{{u.Name}}</td>\
                            <td>{{u.get_Status_display}}</td>\
                            <td>{{u.System}}</td>\
                            <td>{{u.Country}}</td>\
                            <td>{{u.Identify}}</td>\
                        </tr>\
                    {% endfor %}\
                </tbody>\
            </table>''')
        c = Context({'country': obj})
        return t.render(c)

class IdentifyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Status', {
            'fields': ('Name', 'profile',)
        }),
    )

    readonly_fields = ('profile',)

    list_display = ('Name', 'profile',)

admin.site.register(group, GroupAdmin)
admin.site.register(profile, ProfileAdmin)
admin.site.register(checkcode)
admin.site.register(country, CountryAdmin)
admin.site.register(system, SystemAdmin)
admin.site.register(identify, IdentifyAdmin)

