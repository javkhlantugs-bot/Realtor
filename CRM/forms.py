# forms.py
from django import forms
from .models import Event, Clent, Client_suggestion
from django.contrib.contenttypes.models import ContentType

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_type', 'event_date', 'participant_buyer', 'participant_owner', 'event_description','participant_property','event_time']

    event_type = forms.ChoiceField(choices=Event.EVENT_TYPES, widget=forms.Select(attrs={'class': 'form-control'}))
    event_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    event_time = forms.TimeField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'time'}))

class ClientForm(forms.ModelForm):
    class Meta:
        model = Clent
        fields = ['client_name', 'phone_number', 'email']

from Realtor.models import Property, PropertyImage
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_type',
                  'address',
                  'bedrooms',
                  'total_rooms',
                  'toilets',
                  'images',
                  'sqr_meter',
                  'price_sqrm',
                  'condition',
                  'description',
                  'total_floor',
                  'which_floor',
                  'latitude',
                  'longitude']
       
    

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']

PropertyImageFormSet = forms.inlineformset_factory(Property, PropertyImage, form=PropertyImageForm, extra=1, max_num=20, can_delete=False)

class RentalPropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_type',
                  'address',
                  'bedrooms',
                  'total_rooms',
                  'toilets',
                  'images',
                  'sqr_meter',
                  'price_month',
                  'condition',
                  'description',
                  'total_floor',
                  'which_floor',
                  'latitude',
                  'longitude']
       
    

class RentalPropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']

RentalPropertyImageFormSet = forms.inlineformset_factory(Property, PropertyImage, form=RentalPropertyImageForm, extra=1, max_num=20, can_delete=False)

class ClientSuggestionForm(forms.ModelForm):
    class Meta:
        model = Client_suggestion
        fields = ['is_suggested']

    def __init__(self, *args, **kwargs):
        super(ClientSuggestionForm, self).__init__(*args, **kwargs)
        # Add any additional customization if needed

# Assuming your form is defined like this in forms.py
class ClientInterestForm(forms.ModelForm):
    class Meta:
        model = Client_suggestion
        fields = ['is_interested']

    def __init__(self, *args, **kwargs):
        super(ClientInterestForm, self).__init__(*args, **kwargs)

class PropertySuggestionForm(forms.ModelForm):
    class Meta:
        model = Client_suggestion
        fields = ['is_suggested']

    def __init__(self, *args, **kwargs):
        super(ClientSuggestionForm, self).__init__(*args, **kwargs)
