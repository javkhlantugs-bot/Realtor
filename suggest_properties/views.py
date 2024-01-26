# views.py
from django.shortcuts import render, redirect, get_object_or_404
from CRM.forms import ClientInterestForm
from CRM.models import Client_suggestion, Clent
from Realtor.models import Property, PropertyImage
from django.views import View


class ClientSuggestedPropertiesView(View):
    template_name = 'client_suggested_properties.html'

    def get(self, request, client_link):
        client = get_object_or_404(Clent, link=client_link)
        suggestions = Client_suggestion.objects.filter(client=client, is_suggested='suggested')

        return render(request, self.template_name, {'client': client, 'suggestions': suggestions})

    def post(self, request, client_link):
        client = get_object_or_404(Clent, link=client_link)
        suggestions = Client_suggestion.objects.filter(client=client, is_suggested='suggested')

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
        return render(request, self.template_name, {'client': client, 'suggestions': suggestions})
    
def show_property(request, user, id, address):
    property = get_object_or_404(Property, id=id, user__username=user) 
    photos = PropertyImage.objects.filter(property=property)
    fields = Property._meta.fields
    return render(request, 'show_property.html', {
        'properties': property,
        'photos': photos,
        'address': address,
        'fields':fields,
    })