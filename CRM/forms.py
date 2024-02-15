# forms.py
from django import forms
from .models import Event, Clent, Client_suggestion, ClientInterest, client_phone_numbers, client_relationships, event_type_model, suggestion_link_settings, client_status_types
from Realtor.models import Property, property_status,property_type, deal_type
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.forms import modelformset_factory

class EventForm(forms.ModelForm):
    
    event_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    event_hour = forms.ChoiceField(choices=Event.event_hour_choice, widget=forms.Select(attrs={'class': 'form-control','placeholder':'HH'}))
    event_minute = forms.ChoiceField(choices=Event.event_minute_choice, widget=forms.Select(attrs={'class': 'form-control','placeholder':'MM'}))
    event_ampm = forms.ChoiceField(choices=Event.event_ampm_choice, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Event
        fields = ['event_type', 'event_date', 'participant_buyer', 'participant_owner', 'event_description','participant_property','event_hour','event_minute','event_ampm','is_completed']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super(EventForm, self).__init__(*args, **kwargs)

        # Filter choices for participant_buyer
        self.fields['participant_buyer'].queryset = Clent.objects.filter(user=user)
        # Apply 'js-select2' class to participant_buyer field
        self.fields['participant_buyer'].widget.attrs['class'] = 'form-control js-select2'

        # Filter choices for participant_owner
        self.fields['participant_owner'].queryset = Clent.objects.filter(user=user)
        # Apply 'js-select2' class to participant_owner field
        self.fields['participant_owner'].widget.attrs['class'] = 'form-control js-select2'

        # Filter choices for participant_property
        self.fields['participant_property'].queryset = Property.objects.filter(user=user)
        # Apply 'js-select2' class to participant_property field
        self.fields['participant_property'].widget.attrs['class'] = 'form-control js-select2'

        # Filter choices for event_type
        self.fields['event_type'].queryset = event_type_model.objects.filter(user=user)
        # Apply 'js-select2' class to event_type field
        self.fields['event_type'].widget.attrs['class'] = 'form-control js-select2'

class EventTypeForm(forms.ModelForm):
    class Meta:
        model = event_type_model
        fields = ['event_type']

        

class ClientStatusForm(forms.ModelForm):
    class Meta:
        model = client_status_types
        fields = ['status']

class PropertyStatusForm(forms.ModelForm):
    class Meta:
        model = property_status
        fields = ['status']

class PropertyTypeForm(forms.ModelForm):
    class Meta:
        model = property_type
        fields = ['type']

class PropertyDealTypeForm(forms.ModelForm):
    class Meta:
        model = deal_type
        fields = ['deal_type']

        

class ClientForm1(forms.ModelForm):
    class Meta:
        model = Clent
        fields = ['client_name', 'phone_number', 'email','status']

class ClientForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder':'Birthday'}),required=False)
    wedding_anniversary = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder':'Wedding Anniversary'}),required=False)
    home_anniversary = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder':'Home Anniversary'}),required=False)
    class Meta:
        model = Clent
        fields = ['client_name','status','phone_number','email','link','birthday','wedding_anniversary','home_anniversary','facebook_url','instagram_url','twitter_url']

class ClientPhoneNumbers(forms.ModelForm):
    class Meta:
        model = client_phone_numbers
        fields = '__all__'

class ClientRelationships(forms.ModelForm):
    class Meta:
        model = client_relationships
        fields = '__all__'

from Realtor.models import Property, PropertyImage

class PropertyForm1(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['address', 'property_type', 'country', 'postal_code', 'city', 'district', 'sub_district', 'longitude', 'latitude']

        widgets = {
            'address': forms.TextInput(attrs={
                'placeholder': 'Search for address',
                'class': 'controls',
                'id': "pac-input",
                'type': "text",
                'placeholder': "Search Box",
                'name': "property_name",
                'style': "width: 100%;",
                'required': "required",
            
            }),
            'postal_code': forms.TextInput(attrs={'id': 'postal_code','style':'width:100%'}),
            'country': forms.TextInput(attrs={'id': 'country','style':'width:100%'}),
            'city': forms.TextInput(attrs={'id': 'city','style':'width:100%'}),
            'district': forms.TextInput(attrs={'id': 'district','style':'width:100%'}),
            'sub_district': forms.TextInput(attrs={'id': 'sub_district','style':'width:100%'}),
            'longitude': forms.TextInput(attrs={'id': 'longitude','style':'width:100%'}),
            'latitude': forms.TextInput(attrs={'id': 'latitude','style':'width:100%'}),
            
            # Add widgets for other fields as needed
        }

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [  'property_type',
                    'deal_type',
                    'address',
                    'images',
                    'sqr_meter',
                    'price_sqrm',
                    'price_month',
                    'condition',
                    'address_lower',
                    'latitude',
                    'longitude',
                    'lot_size',
                    'monthly_fees',
                    'year_built',
                    'unit',
                    'bedrooms',
                    'status',
                    'total_rooms',
                    'total_price',
                    'toilets',
                    'garage',
                    'fireplace',
                    'dining_room',
                    'living_room',
                    'school_distance',
                    'total_floor',
                    'which_floor',
                    'year_built',
                    'description',
                    'dining_room_description',
                    'living_room_description',
                    'interior_features_description',
                    'exterior_features_description',
                    'style_description',
                    'design_description',
                    'extra_notes',
                    'postal_code',
                    'country',
                    'city',
                    'district',
                    'sub_district',]
        widgets = {
            'condition': forms.TextInput(attrs={'placeholder': 'Enter custom condition'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['condition'].required = False


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'required': False,'multilpe':True}),
        }
        

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

class ClientSuggestionInterestForm(forms.ModelForm):
    class Meta:
        model = Client_suggestion
        fields = ['is_interested']

    def __init__(self, *args, **kwargs):
        super(ClientSuggestionInterestForm, self).__init__(*args, **kwargs)



class ClientInterestForm(forms.ModelForm):
    class Meta:
        model = ClientInterest
        fields = ['note']


class PropertySuggestionForm(forms.ModelForm):
    class Meta:
        model = Client_suggestion
        fields = ['is_suggested']

    def __init__(self, *args, **kwargs):
        super(ClientSuggestionForm, self).__init__(*args, **kwargs)

class suggestion_link_setup(forms.ModelForm):
    class Meta:
        model = suggestion_link_settings
        fields = ['contacts','welcome_message']