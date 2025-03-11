from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, AddressViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register('customers', CustomerViewSet, basename='customer')
router.register('addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('customers', include(router.urls)),
    path('customers/<uuid:pk>/', CustomerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='customer-detail'),
    path('addresses/<int:pk>/', AddressViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='address-detail'),
]
