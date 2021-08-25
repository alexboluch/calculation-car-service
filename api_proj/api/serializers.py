from .models import Calculation
from rest_framework import serializers

class CalculationSerializer(serializers.ModelSerializer):
    broker_forwarding_price = serializers.IntegerField(default=850)
    certification_price = serializers.IntegerField(default=250)
    company_services_price = serializers.IntegerField(default=400)
    url = serializers.URLField(required=False)
    auction = serializers.CharField(default="IAAI")

    class Meta:
        model = Calculation
        read_only_fields = ['id', 'create_date', 'url']
        exclude = ['owner',]

class SearchCalculationSerializer(CalculationSerializer):
        search_field = serializers.CharField()


from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents import CalculationDocument
 
 
class CalculationDocumentSerializer(DocumentSerializer):
    class Meta:
        document = CalculationDocument
        read_only_fields = ['id', 'create_date', 'url']
        exclude = ['owner',]


   
