#coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import User
from django.template import Context, Template
from umunc_iris.models import *
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from import_export import resources
from import_export.admin import ExportActionModelAdmin

from django.forms import ModelForm

from django.forms.widgets import Select

from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

class IdentifyWidget(Select):
    """
    A FileField Widget that shows its current value if it has one.
    """
    def __init__(self, attrs = {}):
        super(IdentifyWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, choices=()):
        output = []
        output.append(super(IdentifyWidget, self).render(name, value, attrs, choices))

        systems = system.objects.all()

        return_str_systems = ''
        for isystem in systems:
            return_str_countrys = ''
            for country in isystem.country_set.all():
                return_str_identifies = ''
                for identify in country.identify_set.all():
                    return_str_identifies += u'''
                        <li>
                            <a tabindex="-1" href="##" onclick="$('#id_Identify').val({1})">{0}</a>
                        </li>
                    '''.format(identify.Name, identify.id)
                return_str_countrys += u'''
                    <li class="dropdown-submenu">
                        <a tabindex="-1" href="##">{0}</a>
                        <ul class="dropdown-menu">
                          {1}
                        </ul>
                    </li>
                '''.format(country.Name, return_str_identifies)
            return_str_systems += u'''
                <li class="dropdown-submenu">
                    <a tabindex="-1" href="##">{0}</a>
                    <ul class="dropdown-menu">
                      {1}
                    </ul>
                </li>
            '''.format(isystem.Name, return_str_countrys)
        return_str = u'''
            <div class="btn-group">
              <a class="btn dropdown-toggle" data-toggle="dropdown" href="#">
                筛选
                <span class="caret"></span>
              </a>
              <ul class="dropdown-menu">
                {0}
              </ul>
            </div>
        '''.format(return_str_systems)

        output.append(return_str)

        return mark_safe(u''.join(output))

class ProfileForm(ModelForm):
    class Meta:
        model = profile
        fields = "__all__"
        # exclude = [] # uncomment this line and specify any field to exclude it from the form
        widgets = {
            'Identify': IdentifyWidget,
        }
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

class GroupResource(resources.ModelResource):
    class Meta:
        model = group
        fields = ('Name', 'School', 'Password', 'Paycode', 'Payment', 'Group')

class ProfileResource(resources.ModelResource):
    def dehydrate_User(self, profile):
        try:
            return u'{}'.format(profile.User.__unicode__())
        except:
            return u'{}'.format(profile.User)

    def dehydrate_Sex(self, profile):
        return u'{}'.format(profile.get_Sex_display())

    def dehydrate_Grade(self, profile):
        return u'{}'.format(profile.get_Grade_display())

    def dehydrate_Commitee(self, profile):
        return u'{}'.format(profile.get_Commitee_display())

    def dehydrate_Commitee2(self, profile):
        return u'{}'.format(profile.get_Commitee2_display())

    def dehydrate_Group(self, profile):
        try:
            return u'{}'.format(profile.Group.__unicode__())
        except:
            return u'{}'.format(profile.Group)

    def dehydrate_Identify(self, profile):
        try:
            return u'{}'.format(profile.Identify.__unicode__())
        except:
            return u'{}'.format(profile.Identify)

    def dehydrate_Interviewer(self, profile):
        try:
            return u'{}'.format(profile.Interviewer.__unicode__())
        except:
            return u'{}'.format(profile.Interviewer)

    class Meta:
        model = profile
        fields = ('User__id', 'User', 'Name', 'Sex', 'Age', 'IDNum', 'School', 'Grade', 'GName', 'GPhone', 'Phone', 'Phone2', 'QQ', 'Wechat', 'Commitee', 'Commitee2', 'Group', 'Identify', 'Review1', 'Review2', 'Review3', 'Review4', 'Interviewer', 'Message', )
        export_order = ('User__id', 'User', 'Name', 'Sex', 'Age', 'IDNum', 'School', 'Grade', 'GName', 'GPhone', 'Phone', 'Phone2', 'QQ', 'Wechat', 'Commitee', 'Commitee2', 'Group', 'Identify', 'Review1', 'Review2', 'Review3', 'Review4', 'Interviewer', 'Message', )

class GroupAdmin(ExportActionModelAdmin):
    fieldsets = (
        ('Basic', {
            'fields': ('Name', 'School', 'Password')
        }),
        ('Status', {
            'fields': ('Paycode', 'Payment', 'Group')
        }),
        ('Command', {
            'classes': ('collapse'),
            'fields': ('sendmail', 'markpayment')
        }),
        ('Member', {
            'classes': ('collapse'),
            'fields': ('member',)
        }),
    )

    list_display = ('Name', 'School', 'Paycode', 'Payment')

    search_fields = ('Name', 'School', 'Paycode', 'Payment',)

    readonly_fields = ('sendmail', 'member', 'markpayment')

    resource_class = GroupResource

    actions_on_top = False
    actions_on_bottom = True

    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('umunc_iris.control_all'):
            return ('sendmail', 'member', 'markpayment')
        else:
            return ('sendmail', 'member', 'Paycode', 'Payment', 'markpayment')

    def sendmail(self, obj):
        return mark_safe(u'''<a target="_blank" class="btn btn-sm btn-default" href=\"/iris/admin/sendmail/?command=sendmail_payment&id='''+str(obj.id)+u'''\">批量发送缴费确认邮件</a>
            ''')

    def markpayment(self, obj):
        return mark_safe(u'''<a target="_blank" class="btn btn-sm btn-default" href=\"/iris/admin/markpayment/?command=markpayment&id='''+str(obj.id)+u'''\">全员标记为已付费并发送邮件，仅影响【代表席位已分配，请进行缴费】的用户</a><br />
            <a target="_blank" class="btn btn-sm btn-default" href=\"/iris/admin/markpayment/?command=unmarkpayment&id='''+str(obj.id)+u'''\">全员标记为未付费，仅影响【代表缴费已完成，申请完成】的用户</a>
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
            return super(GroupAdmin, self).export_admin_action(request, queryset)
        else:
            return HttpResponse(u'<script>alert("无权下载");window.opener=null;window.close();</script>')

    actions = [export_admin_action]

class ProfileAdmin(ExportActionModelAdmin):
    fieldsets = (
        ('Status', {
            'fields': ('User', 'TimeStamp', 'LastMotified', 'Init', 'Status')
        }),
        ('Basic Information', {
            'fields': ('Name', 'Sex', 'Age', 'IDNum', 'School', 'Grade', 'GName', 'GPhone', 'Phone', 'Phone2', 'QQ', 'Wechat', 'MunAge', 'MunRsm', 'Commitee', 'Commitee2', 'Adjust', 'Message')
        }),
        ('Group Information', {
			'classes': ('collapse'),
            'fields': ('Group', 'Leader')
        }),
        ('Distribution', {
			'classes': ('collapse'),
            'fields': ('Identify',)
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
        ('Interviewee', {
            'classes': ('collapse'),
            'fields': ('interviewee',)
        }),
    )

    form = ProfileForm

    list_display = ('User', 'Name', 'Status', 'Group', 'Commitee', 'Identify')

    search_fields = ('User__username', 'Name', 'School', 'Phone', 'Phone2', 'Group__Paycode')

    list_filter = ('Status', 'Group', 'School', 'Identify', 'Commitee', 'Commitee2',)

    resource_class = ProfileResource

    actions_on_top = False
    actions_on_bottom = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "Interviewer":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super(ProfileAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('umunc_iris.control_all'):
            return ('TimeStamp', 'LastMotified', 'sendmail', 'interviewee')
        else:
            return ('TimeStamp', 'LastMotified', 'Init', 'Status', 'Name', 'Sex', 'Age', 'IDNum', 'School', 'Grade', 'GName', 'GPhone', 'Phone', 'Phone2', 'QQ', 'Wechat', 'MunAge', 'MunRsm', 'Commitee', 'Commitee2', 'Adjust', 'Group', 'Leader', 'Review1', 'Review2', 'Review3', 'Review4', 'sendmail', 'interviewee', 'Message')

    def sendmail(self, obj):
        return mark_safe(u'''<a target="_blank" class="btn btn-sm btn-default" href=\"/iris/admin/sendmail/?command=sendmail_emailcheck&id='''+str(obj.User.id)+u'''\">发送注册邮件</a><br/>
            <a target="_blank" class="btn btn-sm btn-default" href=\"/iris/admin/sendmail/?command=sendmail_interview&id='''+str(obj.User.id)+u'''\">发送面试通知邮件</a><br/>
            <a target="_blank" class="btn btn-sm btn-default" href=\"/iris/admin/sendmail/?command=sendmail_interview_reject&id='''+str(obj.User.id)+u'''\">发送面试重分配通知邮件</a><br/>
            <a target="_blank" class="btn btn-sm btn-default" href=\"/iris/admin/sendmail/?command=sendmail_identify&id='''+str(obj.User.id)+u'''\">发送席位通知邮件</a><br/>
            <a target="_blank" class="btn btn-sm btn-default" href=\"/iris/admin/sendmail/?command=sendmail_payment_user&id='''+str(obj.User.id)+u'''\">发送缴费确认邮件</a>
            ''')

    def interviewee(self, obj):
        t = Template(u'''<table class="table table-striped table-hover table-bordered">\
                <thead>\
                    <th>被面试用户名</th>\
                    <th>姓名</th>\
                    <th>状态</th>\
                    <th>席位 席位名称</th>\
                </thead>\
                <tbody>\
                    {% for u in profile.User.Interviewee.all %}\
                        <tr class="\
                            {% if u.Status > 5 %}success{% endif %}\
                            {% if u.Status < 0 %}danger{% endif %}\
                        ">\
                            <td><a href="/admin/umunc_iris/profile/{{u.id}}/">{{u.User.username}}</td>\
                            <td>{{u.Name}}</td>\
                            <td>{{u.get_Status_display}}</td>\
                            <td>{{u.Identify}}</td>\
                        </tr>\
                    {% endfor %}\
                </tbody>\
            </table>''')
        c = Context({'profile': obj})
        return t.render(c)


class CountryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Status', {
            'fields': ('Name', 'System')
        }),
        ('Member', {
            'classes': ('collapse'),
            'fields': ('member',)
        }),
    )

    list_filter = ('System', 'Name',)

    readonly_fields = ('member',)

    list_display = ('__unicode__', 'Name',)

    def member(self, obj):
        t = Template(u'''<table class="table table-striped table-hover table-bordered">\
                <thead>\
                    <th>用户名</th>\
                    <th>姓名</th>\
                    <th>状态</th>\
                    <th>席位 席位名称</th>\
                </thead>\
                <tbody>\
                    {% for i in country.identify_set.all %}\
                        <tr class="\
                            {% if i.profile.Status > 5 %}success{% endif %}\
                            {% if i.profile.Status < 0 %}danger{% endif %}\
                        ">\
                            <td><a href="/admin/umunc_iris/profile/{{i.profile.id}}/">{{i.profile.User.username}}</td>\
                            <td>{{i.profile.Name}}</td>\
                            <td>{{i.profile.get_Status_display}}</td>\
                            <td>{{i.profile.Identify}}</td>\
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
                    <th>席位 席位名称</th>\
                </thead>\
                <tbody>\
                    {% for c in system.country_set.all %}
                    {% for i in c.identify_set.all %}\
                        <tr class="\
                            {% if i.profile.Status > 5 %}success{% endif %}\
                            {% if i.profile.Status < 0 %}danger{% endif %}\
                        ">\
                            <td><a href="/admin/umunc_iris/profile/{{i.profile.id}}/">{{i.profile.User.username}}</td>\
                            <td>{{i.profile.Name}}</td>\
                            <td>{{i.profile.get_Status_display}}</td>\
                            <td>{{i.profile.Identify}}</td>\
                        </tr>\
                    {% endfor %}\
                    {% endfor %}\
                </tbody>\
            </table>''')
        c = Context({'system': obj})
        return t.render(c)

class IdentifyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Status', {
            'fields': ('Name', 'Country', 'profile',)
        }),
    )

    list_filter = ('Country__System', 'Country', 'Name',)

    readonly_fields = ('profile',)

    list_display = ('__unicode__', 'Name', 'profile',)

admin.site.register(group, GroupAdmin)
admin.site.register(profile, ProfileAdmin)
admin.site.register(checkcode)
admin.site.register(country, CountryAdmin)
admin.site.register(system, SystemAdmin)
admin.site.register(identify, IdentifyAdmin)
