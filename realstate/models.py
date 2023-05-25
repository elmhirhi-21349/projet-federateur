from django.db import models
# Create your models here.

class BiensImmobilier(models.Model):
    nom = models.CharField(max_length=255, blank=True, null=True)
    site = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    localisation = models.CharField(max_length=255, blank=True, null=True)
    prix = models.DecimalField(max_digits=99999, decimal_places=3, blank=True, null=True)
    pieces = models.CharField(max_length=255, blank=True, null=True)
    superficie = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    page = models.CharField(max_length=50, blank=True, null=True)

