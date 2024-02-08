from django.db import models
from accounts.models import CustomUser

class LinkModel(models.Model):
    url = models.URLField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class Property(models.Model):
    PROPERTY_TYPES = (
        ('office', 'Office'),
        ('apartment', 'Apartment'),
        ('house', 'House'),
    )

    DEAL_TYPE = (
        ('rental', 'Rental'),
        ('selling', 'Selling'),
    )

    STATUS_CHOICES = (
        ('active',"Active"),
        ('cancelled','Cancelled'),
    )

    CONDITION_CHOICES = (
        ('cash', 'Бэлэн'),
        ('barter', 'Бартер'),
        ('Leasing','Лизинг'),
        ('3 plus 1','3 + 1'),
        ('6 plus 1','6 + 1'),
        ('12 plus 1','12 + 1'),
        ('1 plus 1','1 + 1'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, blank=True, null = True)
    deal_type = models.CharField(max_length=10, choices=DEAL_TYPE, blank=True, null = True)
    address = models.CharField(max_length=255, blank=True, null = True)
    images = models.ImageField(blank=True, null=True)
    sqr_meter = models.IntegerField(blank=True, null = True)
    price_sqrm = models.FloatField(null=True, blank = True)
    price_month = models.FloatField(null=True, blank = True)
    condition = models.CharField(max_length=20, blank=True, null = True)
    address_lower = models.CharField(max_length=255, blank=True, null = True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    listing_date = models.DateField(null = True,blank = True)
    lot_size = models.IntegerField(null=True, blank=True)
    monthly_fees = models.IntegerField(null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=30,choices=STATUS_CHOICES,blank=True, null= True)

    bedrooms = models.IntegerField(blank=True, null = True)
    total_rooms = models.IntegerField(blank=True, null = True)
    toilets = models.IntegerField(blank=True, null = True)
    garage = models.IntegerField(blank=True, null = True)
    fireplace = models.IntegerField(blank=True, null = True)
    dining_room = models.IntegerField(blank=True, null = True)
    living_room = models.IntegerField(blank=True, null = True)
    school_distance = models.IntegerField(blank=True, null = True)

    total_floor = models.IntegerField(blank=True, null = True)
    which_floor = models.IntegerField(blank=True, null = True)
    year_built = models.IntegerField(null=True, blank=True)

    description = models.TextField(blank=True, null = True)
    dining_room_description = models.TextField(blank=True, null = True)
    living_room_description = models.TextField(blank=True, null = True)
    interior_features_description = models.TextField(blank=True, null = True)
    exterior_features_description = models.TextField(blank=True, null = True)
    style_description = models.TextField(blank=True, null = True)
    design_description = models.TextField(blank=True, null = True)
    extra_notes = models.TextField(blank=True, null = True)

    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    sub_district = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Save the lowercase version of the address
        self.address_lower = self.address.lower()
        super().save(*args, **kwargs)

    
    @property
    def name(self):
        if self.total_price:
            return f"{self.address} - {self.total_price}"
        else:
            return self.address

    def __str__(self):
        return self.name
            
    
class PropertyImage(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"{self.property.deal_type} - {self.property.address}"
