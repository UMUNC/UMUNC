from django.contrib import admin
from umunc_cheetah.models import *
from django import forms
from searchableselect.widgets import SearchableSelect

class MyModelForm(forms.ModelForm):
    class Meta:
        model = room
        exclude = ()
        widgets = {
            'User': SearchableSelect(model='auth.User', search_field='profile__Name profile__Identify__Name profile__Identify__Country__Name profile__Identify__Country__System__Name', many=True)
        }

class MyModelAdmin(admin.ModelAdmin):
    form = MyModelForm

admin.site.register(room, MyModelAdmin)
admin.site.register(message)
admin.site.register(meeting)
