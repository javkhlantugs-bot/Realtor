# forms.py
from django import forms
from .models import Event, Clent, Client_suggestion, ClientInterest
from Realtor.models import Property
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class EventForm(forms.ModelForm):

    event_type = forms.ChoiceField(choices=Event.EVENT_TYPES, widget=forms.Select(attrs={'class': 'form-control'}))
    event_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    event_time = forms.TimeField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'time'}))

    class Meta:
        model = Event
        fields = ['event_type', 'event_date', 'participant_buyer', 'participant_owner', 'event_description','participant_property','event_time']
    
class ClientForm(forms.ModelForm):
    class Meta:
        model = Clent
        fields = ['client_name', 'phone_number', 'email','status']

from Realtor.models import Property, PropertyImage
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
        widgets = {
            'condition': forms.TextInput(attrs={'placeholder': 'Enter custom condition'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add the default choices to the condition field
        self.fields['condition'].widget.choices = Property.CONDITION_CHOICES
        self.fields['condition'].required = False
    

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

class ClientInterestForm(forms.ModelForm):
    class Meta:
        model = ClientInterest
        exclude = ['user', 'date_added']

    def __init__(self, user, *args, **kwargs):
        super(ClientInterestForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super(ClientInterestForm, self).save(commit=False)
        instance.user = self.user
        instance.date_added = timezone.now()

        if commit:
            instance.save()

        return instance

class PropertySuggestionForm(forms.ModelForm):
    class Meta:
        model = Client_suggestion
        fields = ['is_suggested']

    def __init__(self, *args, **kwargs):
        super(ClientSuggestionForm, self).__init__(*args, **kwargs)
