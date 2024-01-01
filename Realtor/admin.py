from django.contrib import admin
from django import forms
from .models import LinkModel, Property, PropertyImage

@admin.register(LinkModel)
class LinkModelAdmin(admin.ModelAdmin):
    pass

class PropertyImageAdmin(admin.TabularInline):  # Use TabularInline for a more compact display
    model = PropertyImage

    
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageAdmin]  # Use the correct attribute name 'inlines'
    
    list_display = ('property_type', 'deal_type', 'address', 'bedrooms')  # Customize the list display

    def image_count(self, obj):
        return obj.images.count()  # Display the count of associated images in the list view

    image_count.short_description = 'Image Count'  # Set a custom column header

    class Meta:
        model = Property


admin.site.register(Property, PropertyAdmin)


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    pass

#-----
