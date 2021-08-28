from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CalculationSerializer
from .models import Calculation
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .backends import CsrfExemptSessionAuthentication
from .logics import create_logic
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from .models import User
from rest_framework import filters

class IsOwner(permissions.BasePermission):


    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        elif view.kwargs.get('pk'):
            obj = Calculation.objects.get(pk=view.kwargs['pk'])
            return obj.owner == request.user
        else:
            return True


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CalculationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [CsrfExemptSessionAuthentication, JWTAuthentication]
    pagination_class = StandardResultsSetPagination
    queryset = Calculation.objects.all()

    def list(self, request):
        if request.user.is_staff:
            queryset = Calculation.objects.all()
        else:
            queryset = Calculation.objects.all().filter(owner=request.user)
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = CalculationSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = CalculationSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    
    def retrieve(self, request, pk=None):
        queryset = Calculation.objects.all()
        calculation = get_object_or_404(queryset, pk=pk)
        # calculation = self.get_object()
        self.check_object_permissions(request, calculation)
        serializer = CalculationSerializer(calculation)
        serializer.data["url"] = calculation.url
        return Response(serializer.data)


    def create(self, request):
        data = request.data
        serializer = CalculationSerializer(data=data)
        if serializer.is_valid():
            username=request.user.username
            user = User.objects.get(username=username)
            commission_price, swift_price, registration_price, delivery_land_price, delivery_all_price, customs_clearance_price, end_price = create_logic(serializer)
            serializer.save(
            commission_price=commission_price,
            swift_price = swift_price,
            registration_price=registration_price,
            delivery_land_price=delivery_land_price,
            delivery_all_price=delivery_all_price,
            customs_clearance_price=customs_clearance_price,
            end_price=end_price,
            owner=user,
            )
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


    def get_attr_or_update(self, obj, serializer, attr):
        try:
            upd_attr = serializer.validated_data[attr]
        except:
            serializer.validated_data[attr] = getattr(obj, attr)


    def update(self, request, pk=None):
        calculation = Calculation.objects.get(pk=pk)
        serializer = CalculationSerializer(calculation, data=request.data)
        if serializer.is_valid():
            commission_price, swift_price, registration_price, delivery_land_price, delivery_all_price, customs_clearance_price, end_price = create_logic(serializer)
            serializer.save(
            commission_price=commission_price,
            swift_price = swift_price,
            registration_price=registration_price,
            delivery_land_price=delivery_land_price,
            delivery_all_price=delivery_all_price,
            customs_clearance_price=customs_clearance_price,
            end_price=end_price
            )
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


    def partial_update(self, request, pk=None):
        calculation = Calculation.objects.get(pk=pk)
        serializer = CalculationSerializer(calculation, data=request.data, partial=True)
        if serializer.is_valid():
            self.get_attr_or_update(calculation, serializer, 'year')
            self.get_attr_or_update(calculation, serializer, 'engine')
            self.get_attr_or_update(calculation, serializer, 'auction_price')
            self.get_attr_or_update(calculation, serializer, 'distance_to_port')
            self.get_attr_or_update(calculation, serializer, 'delivery_sea_price')
            self.get_attr_or_update(calculation, serializer, 'broker_forwarding_price')
            self.get_attr_or_update(calculation, serializer, 'certification_price')
            self.get_attr_or_update(calculation, serializer, 'company_services_price')

            commission_price, swift_price, registration_price, delivery_land_price, delivery_all_price, customs_clearance_price, end_price = create_logic(serializer)
            serializer.save(
            commission_price=commission_price,
            swift_price = swift_price,
            registration_price=registration_price,
            delivery_land_price=delivery_land_price,
            delivery_all_price=delivery_all_price,
            customs_clearance_price=customs_clearance_price,
            end_price=end_price
            )
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


    def destroy(self, request, pk=None):
        calculation = Calculation.objects.get(pk=pk)
        calculation.delete()
        return JsonResponse({"message": "Object was deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


class SearchView(ListAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [CsrfExemptSessionAuthentication, JWTAuthentication]
    pagination_class = StandardResultsSetPagination
    serializer_class = CalculationSerializer
    # serializer_class = SearchCalculationSerializer
    queryset = Calculation.objects.all()
    search_fields = ['title', 'comment']
    filter_backends = (filters.SearchFilter,)



    # def get(self, request, *args, **kwargs):
    #     search_field = request.query_params.get("search_field")
    #     if search_field is None:
    #         queryset = Calculation.objects.all().filter(owner=1)
    #     else:
    #         queryset = Calculation.objects.all().filter(search_field=search_field)
    #     return self.list(request, *args, **kwargs)



# from django_elasticsearch_dsl_drf.constants import (
#     LOOKUP_FILTER_RANGE,
#     LOOKUP_QUERY_IN,
#     LOOKUP_QUERY_GT,
#     LOOKUP_QUERY_GTE,
#     LOOKUP_QUERY_LT,
#     LOOKUP_QUERY_LTE,
# )
# from django_elasticsearch_dsl_drf.filter_backends import (
#     FilteringFilterBackend,
#     OrderingFilterBackend,
#     DefaultOrderingFilterBackend,
#     SearchFilterBackend,
# )
# from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
 
# from .documents import CalculationDocument
# from .serializers import CalculationDocumentSerializer
