from .views import create_calculation, main_view, calc_update, registration
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf.urls import url


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('main/', main_view),
    path('add_calc/', create_calculation),
    # path('calc_detail/<uuid:pk>/', calc_update, name='calc_detail'),
    path('calc_detail/<uuid:pk>/', calc_update, name='calc_detail'),
    path('reg/', registration),
    path('', RedirectView.as_view(url='/main/', permanent=True)),
]
