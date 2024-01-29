# views.py
from django.shortcuts import render, redirect, get_object_or_404
from CRM.forms import ClientInterestForm
from CRM.models import Client_suggestion, Clent, suggestion_link_settings
from accounts.models import CustomUser
from Realtor.models import Property, PropertyImage
from django.views import View


class ClientSuggestedPropertiesView(View):
    template_name = 'client_suggested_properties.html'

    def get(self, request, client_link, user):
        client = get_object_or_404(Clent, link=client_link)
        suggestions = Client_suggestion.objects.filter(client=client, is_suggested='suggested')
        userid = get_object_or_404(CustomUser,  username=user)
        setups = suggestion_link_settings.objects.get(user=userid.id)
        locations = list(suggestions.values('property__user','property__latitude', 'property__longitude', 'property__deal_type','property__property_type',
                               'property__total_rooms', 'property__address', 'property__id'))
        return render(request, self.template_name, {'client': client, 'suggestions': suggestions,'locations':locations,'user':user,'setups':setups})

    def post(self, request, client_link,user):
        client = get_object_or_404(Clent, link=client_link)
        suggestions = Client_suggestion.objects.filter(client=client, is_suggested='suggested')
        locations = list(suggestions.values('property__user','property__latitude', 'property__longitude', 'property__deal_type','property__property_type',
                               'property__total_rooms', 'property__address', 'property__id'))
        userid = get_object_or_404(CustomUser,  username=user)
        setups = suggestion_link_settings.objects.get(user=userid.id)
        if 'is_interested' in request.POST:
            suggestion_id = request.POST.get('suggestion_id')
            suggestion = get_object_or_404(Client_suggestion, id=suggestion_id)

            # Use the ClientSuggestionForm for the is_interested field
            form = ClientInterestForm(request.POST, instance=suggestion)

            if form.is_valid():
                form.save()
                # Add any additional logic after saving the form if needed
            else:
                # Handle form validation errors if necessary
                pass

        # You may want to redirect or render a response after processing the POST request
        return render(request, self.template_name, {'client': client, 'suggestions': suggestions,'locations':locations,'user':user,'setups':setups})
    
def show_property(request, user, id, address):
    property = get_object_or_404(Property, id=id, user__username=user) 
    locations = list(Property.objects.values('latitude', 'longitude','id').filter(user=request.user.id, id = id))
    photos = PropertyImage.objects.filter(property=property)
    fields = Property._meta.fields
    return render(request, 'show_property.html', {
        'properties': property,
        'photos': photos,
        'address': address,
        'fields':fields,
        'locations':locations
    })