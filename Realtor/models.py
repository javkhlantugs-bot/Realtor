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
        
        # Add more property types as needed
    )

    DEAL_TYPE = (
        ('rental', 'Rental'),
        ('selling', 'Selling'),
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
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    deal_type = models.CharField(max_length=10, choices=DEAL_TYPE)
    address = models.CharField(max_length=255)
    bedrooms = models.IntegerField()
    total_rooms = models.IntegerField()
    toilets = models.IntegerField()
    images = models.ImageField(blank=True)
    sqr_meter = models.IntegerField()
    price_sqrm = models.FloatField(null=True)
    price_month = models.FloatField(null=True)
    condition = models.CharField(max_length = 20, choices = CONDITION_CHOICES)
    description = models.TextField()
    # New field to store the lowercase version of the address
    address_lower = models.CharField(max_length=255, editable=False)
    total_floor = models.IntegerField()
    which_floor = models.IntegerField()
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    @property
    def total_price(self):
        return self.price_sqrm * self.sqr_meter

    def save(self, *args, **kwargs):
        # Save the lowercase version of the address
        self.address_lower = self.address.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.deal_type} - {self.address}"
    
class PropertyImage(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"{self.property.deal_type} - {self.property.address}"
