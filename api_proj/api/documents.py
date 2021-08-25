from elasticsearch_dsl import analyzer
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Index, fields 
from .models import Calculation

# html_strip = analyzer(
#     'html_strip',
#     tokenizer="standard",
#     filter=["standard", "lowercase", "stop", "snowball"],
#     char_filter=["html_strip"]
# )  

@registry.register_document
class CalculationDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'calculations'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Calculation # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = (
            'title',
            'comment',
        )
        # fields = (
        #     'id',
        #     'auction',
        #     'year',
        #     'engine',
        #     'auction_price',
        #     'commission_price',
        #     'swift_price',
        #     'distance_to_port',
        #     'delivery_sea_price',
        #     'certification_price',
        #     'registration_price',
        #     'broker_forwarding_price',
        #     'company_services_price',
        #     'comment',
        #     'create_date',
        #     'delivery_land_price',
        #     'customs_clearance_price',
        #     'delivery_all_price',
        #     'end_price',
        # )

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        queryset_pagination = 5

