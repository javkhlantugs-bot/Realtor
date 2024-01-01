# CRM/admin.py
from django.contrib import admin
from .models import Clent, Event, Client_suggestion
from django import forms

class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the fields of the related Client optional
        self.fields['participant_buyer'].required = False
        self.fields['participant_owner'].required = False

class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm

admin.site.register(Clent)
admin.site.register(Event, EventAdmin)


admin.site.register(Client_suggestion)