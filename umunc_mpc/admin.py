from django.contrib import admin
from umunc_mpc.models import *
from django import forms
from searchableselect.widgets import SearchableSelect

class MyModelForm(forms.ModelForm):
    class Meta:
        model = Press
        exclude = ()
        widgets = {
            'user': SearchableSelect(model='auth.User', search_field='profile__Name profile__Identify__Name profile__Identify__Country__Name profile__Identify__Country__System__Name', many=True)
        }

class MyModelAdmin(admin.ModelAdmin):
    form = MyModelForm

admin.site.register(Press, MyModelAdmin)

admin.site.register(Post)
