from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import LinkModel, Property, PropertyImage
# Create your views here.

def home(request):
    
    return render(request, 'home.html')

def about(request):
    return render(request, "about.html")

def properties(request):
    return render(request, "properties.html")

def services(request):
    # Fetch links from the database
    links = LinkModel.objects.all()

    # Pass links to the template
    context = {'links': links}
    return render(request, "services.html", context)

def client_resources(request):
    return render(request, "client_resources.html")

def rent_properties(request):
    properties_for_rent = Property.objects.filter(deal_type='rental')
    # Get filter values from the request
    property_type_filter = request.GET.get('property_type', '')
    availability_filter = request.GET.get('availability', '')
    condition_filter = request.GET.get('condition', '')
    search_query = request.GET.get('search', '')
    search_query = search_query.lower()

    # Apply filters if values are provided
    if property_type_filter:
        properties_for_rent = properties_for_rent.filter(property_type=property_type_filter)
    if availability_filter:
        properties_for_rent = properties_for_rent.filter(availability=availability_filter)
    if condition_filter:
        properties_for_rent = properties_for_rent.filter(condition=condition_filter)
    if search_query:
        # Use case-insensitive search by comparing lowercase values
        properties_for_rent = properties_for_rent.filter(address_lower__icontains=search_query)

    return render(
        request,
        'rent_properties.html',
        {
            'propertys': properties_for_rent,
            'property_type_filter': property_type_filter,
            'availability_filter': availability_filter,
            'condition_filter': condition_filter,
            'search_query': search_query,
        }
    )

def to_rent_properties(request):
    return render(request, 'to_rent_properties.html')

def sell_properties(request):
    return render(request, "sell_properties.html")
def buy_properties(request):
    properties_for_sale = Property.objects.filter(deal_type='selling')

    # Get filter values from the request
    property_type_filter = request.GET.get('property_type', '')
    availability_filter = request.GET.get('availability', '')
    condition_filter = request.GET.get('condition', '')
    search_query = request.GET.get('search', '')
    search_query = search_query.lower()

    # Apply filters if values are provided
    if property_type_filter:
        properties_for_sale = properties_for_sale.filter(property_type=property_type_filter)
    if availability_filter:
        properties_for_sale = properties_for_sale.filter(availability=availability_filter)
    if condition_filter:
        properties_for_sale = properties_for_sale.filter(condition=condition_filter)
    if search_query:
        # Use case-insensitive search by comparing lowercase values
        properties_for_sale = properties_for_sale.filter(address_lower__icontains=search_query)

    return render(
        request,
        'buy_properties.html',
        {
            'propertys': properties_for_sale,
            'property_type_filter': property_type_filter,
            'availability_filter': availability_filter,
            'condition_filter': condition_filter,
            'search_query': search_query,
        }
    )
def detail_view(request, id):
    property = get_object_or_404(Property, id=id)
    photos = PropertyImage.objects.filter(property=property)
    return render(request, 'details.html', {
        'properties':property,
        'photos':photos
    })

def detail_view_rental(request, id):
    property = get_object_or_404(Property, id=id)
    photos = PropertyImage.objects.filter(property=property)
    return render(request, 'detailsRental.html', {
        'properties':property,
        'photos':photos
    })
