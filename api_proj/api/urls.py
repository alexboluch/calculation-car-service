from django.urls import path,include, re_path           
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import CalculationViewSet, SearchView

router = DefaultRouter()
router.register(r'calculations', CalculationViewSet, basename="calculation")
urlpatterns = router.urls

urlpatterns += path('search/', SearchView.as_view(), name='calculations_search'),


