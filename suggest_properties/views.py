# views.py
from django.shortcuts import render, redirect, get_object_or_404
from CRM.forms import ClientSuggestionInterestForm
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
                               'property__total_rooms', 'property__address', 'property__id','property__total_price'))
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

            form = ClientSuggestionInterestForm(request.POST, instance=suggestion)

            if form.is_valid():
                form.save()
            else:
                print(form.errors)
                pass

        return render(request, self.template_name, {'client': client, 'suggestions': suggestions,'locations':locations,'user':user,'setups':setups})
    
def show_property(request, user, id, address):
    property = get_object_or_404(Property, id=id, user__username=user) 
    suggestions = Client_suggestion.objects.filter(property=property, is_suggested='suggested')
    locations = list(Property.objects.values('latitude', 'longitude','id').filter(user=request.user.id, id = id))
    photos = PropertyImage.objects.filter(property=property)
    fields = Property._meta.fields
    property.views_count += 1
    property.save()
    return render(request, 'show_property.html', {
        'properties': property,
        'photos': photos,
        'address': address,
        'fields':fields,
        'locations':locations,
        'suggestions':suggestions
    })



class TotalListView(View):
    template_name = 'total_list.html'

    def get(self, request, user):
        userid = get_object_or_404(CustomUser,  username=user)
        suggestions = Property.objects.filter(user=userid.id)
        setups = suggestion_link_settings.objects.get(user=userid.id)
        locations = list(suggestions.values('user','latitude', 'longitude', 'deal_type','property_type',
                               'total_rooms', 'address', 'id','total_price'))
        return render(request, self.template_name, {'locations':locations,'user':user,'setups':setups,'suggestions':suggestions})

    