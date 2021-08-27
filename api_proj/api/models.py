
from django.db import models
from django.db.models.query_utils import PathInfo
from django.urls import reverse
from django.contrib.auth.models import User
from django.urls import reverse
from web.logics import create_loan_year, create_loan_engine

import uuid
from django.conf import settings

class Calculation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50, null=True, blank=True, help_text='Calculation title')
    LOAN_AUCTION = (
        ("copart", "Copart"),
        ("iaai", "IAAI",)
    )
    auction = models.CharField(max_length=10, null=True, blank=True, choices=LOAN_AUCTION, help_text='Copart or IAAI', default="IAAI")
    LOAN_YEAR = create_loan_year(2000)
    year = models.IntegerField(choices=LOAN_YEAR, help_text='Year is required')
    LOAN_ENGINE = create_loan_engine(1000, 3500)
    engine = models.IntegerField(choices=LOAN_ENGINE, help_text='Engine is required')
    auction_price = models.IntegerField(help_text='Buy price is required')
    commission_price = models.IntegerField(null=True, blank=True, help_text='Auto-calculation field')
    swift_price = models.IntegerField(null=True, blank=True, help_text='Auto-calculation field')
    distance_to_port = models.IntegerField(help_text='Distance to port is required')
    delivery_land_price = models.IntegerField(null=True, blank=True, help_text='Auto-calculation field')
    delivery_sea_price = models.IntegerField(help_text='Delivery sea price is required')
    delivery_all_price = models.IntegerField(null=True, blank=True, help_text='Auto-calculation field')
    customs_clearance_price = models.IntegerField(null=True, blank=True, help_text='Auto-calculation field')
    broker_forwarding_price = models.IntegerField(help_text='Auto-calculation field')
    certification_price = models.IntegerField(help_text='Auto-calculation field')
    company_services_price = models.IntegerField(help_text='How many profit?')
    registration_price = models.IntegerField(null=True, blank=True, help_text='Auto-calculation field')
    end_price = models.IntegerField(null=True, blank=True, help_text='Auto-calculation field')
    comment = models.CharField(max_length=100, null=True, blank=True, help_text='Few words about this')
    create_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return self.title + ", " + str(self.engine) + ", " + str(self.year)

    def get_absolute_url(self):
        return reverse ('calc_detail', args = [str(self .id)])

    def get_relative_url(self):
        return '/calc_detail/' + str(self .id)
    
    
    def get_api_url(self):
        return settings.SITE_URL + "/api/calculations/" + str(self.id) + "/"


    def get_full_name(self):
        return self.title + ", " + str(self.engine/1000) + "L, " + str(self.year) + " year, $" + str(self.end_price) + ", " + self.create_date.strftime("%d %B")

    
    def get_search_field(self):
        search = self.title + " " + str(self.engine) + " " + str(self.year) + " " + str(self.comment)
        return search

    def get_str_date(self):
        return self.create_date.strftime("%d %B")

    def get_delete_url(self):
        return '/calc_detail/' + str(self .id) + "/delete/"
    

    search_field = property(get_search_field)

    url = property(get_api_url)


