from django.db import models
from cloudinary.models import CloudinaryField


# Create your models here.
class Category(models.Model):


    class Meta:
        verbose_name_plural = 'Categories'


    name = models.CharField(max_length=180)
    friendly_name = models.CharField(max_length=180, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=180)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    collection = models.CharField(max_length=100, null=True, blank=True)
    image = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.name