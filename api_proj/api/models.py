
from django.db import models
from django.db.models.query_utils import PathInfo
from django.urls import reverse
from django.contrib.auth.models import User

import uuid
from django.conf import settings

class Calculation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50, null=True, blank=True)
    auction = models.CharField(max_length=10, null=True, blank=True)
    year = models.IntegerField()
    engine = models.IntegerField()
    auction_price = models.IntegerField()
    commission_price = models.IntegerField(null=True, blank=True)
    swift_price = models.IntegerField(null=True, blank=True)
    distance_to_port = models.IntegerField()
    delivery_land_price = models.IntegerField(null=True, blank=True)
    delivery_sea_price = models.IntegerField()
    delivery_all_price = models.IntegerField(null=True, blank=True)
    customs_clearance_price = models.IntegerField(null=True, blank=True)
    broker_forwarding_price = models.IntegerField(default=850)
    certification_price = models.IntegerField(default=250)
    company_services_price = models.IntegerField(default=400)
    registration_price = models.IntegerField(null=True, blank=True)
    end_price = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=100, null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return self.title + ", " + str(self.engine) + ", " + str(self.year)
    
    
    def get_url(self):
        return settings.SITE_URL + "/api/calculations/" + str(self.id) + "/"


    def get_full_name(self):
        return self.title + ", " + str(self.engine) + ", " + str(self.year)

    
    def get_search_field(self):
        search = self.title + " " + str(self.engine) + " " + str(self.year) + " " + str(self.comment)
        return search
    
    search_field = property(get_search_field)

    url = property(get_url)


