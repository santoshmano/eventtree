"""All the vendors related models goes here """
from django.db import models

from selebmvp.user_profile.models import SelebUser


class Vendor(models.Model):
    slug = models.CharField(max_length=250)
    name = models.CharField(max_length=245)
    website = models.CharField(max_length=250, blank=True, null=True)
    owner = models.ForeignKey(SelebUser, related_name='businesses')
    users = models.ManyToManyField(SelebUser)

    def __str__(self):
        return self.name


class VendorAddress(models.Model):
    addressline1 = models.CharField(max_length=250)
    addressline2 = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150, default='California')
    zipcode = models.CharField(max_length=5)
    vendor = models.OneToOneField(Vendor)


class VendorPhoto(models.Model):
    title = models.CharField(max_length=250)
    key = models.CharField(max_length=250)
    vendor = models.ForeignKey(Vendor, related_name='photos')

    def __str__(self):
        return self.title


class VendorSocialReview(models.Model):
    site = models.CharField(max_length=150)
    num_reviews = models.IntegerField(verbose_name='Number of Reviews')
    rating = models.IntegerField(verbose_name='Rating')
    link = models.CharField(max_length=250)
    vendor = models.ForeignKey(Vendor)


class VendorService(models.Model):
    price_types = (
        ('PH', 'Per Hour'),
        ('PP', 'Per Person'),
        ('PS', 'Per Service')
    )

    title = models.CharField(max_length=250)
    short_desc = models.CharField(max_length=500)
    contact_user = models.ForeignKey(
        SelebUser, related_name='managed_services')
    price_type = models.CharField(choices=price_types, max_length=2)
    price = models.FloatField()
    detailed_desc = models.TextField()
    duration = models.CharField(max_length=10)
    min_people = models.IntegerField(verbose_name='Minimum Number of People')
    max_people = models.IntegerField(verbose_name='Maximum Number of People')


class VendorServicePhoto(models.Model):
    title = models.CharField(max_length=250)
    key = models.CharField(max_length=250)
    vendor_service = models.ForeignKey(VendorService, related_name='photos')


class LocationAmenity(models.Model):
    amenity = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class CateringAmenity(models.Model):
    amenity = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class VendorLocationService(VendorService):
    amenities = models.ManyToManyField(LocationAmenity)
    vendor = models.ForeignKey(Vendor)


class VendorCateringService(VendorService):
    amenities = models.ManyToManyField(CateringAmenity)
    vendor = models.ForeignKey(Vendor)
