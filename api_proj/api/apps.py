from django.apps import AppConfig
from django.conf import settings
import os

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    path = os.path.join(settings.BASE_DIR, name)
