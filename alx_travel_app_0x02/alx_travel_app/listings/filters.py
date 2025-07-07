import django_filters
from .models import Listing, Booking

class ListingFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='lte')
    min_bedrooms = django_filters.NumberFilter(field_name='bedrooms', lookup_expr='gte')
    min_bathrooms = django_filters.NumberFilter(field_name='bathrooms', lookup_expr='gte')
    min_guests = django_filters.NumberFilter(field_name='max_guests', lookup_expr='gte')
    
    class Meta:
        model = Listing
        fields = {
            'property_type': ['exact'],
            'status': ['exact'],
            'city': ['icontains'],
            'country': ['icontains'],
            'bedrooms': ['exact'],
            'bathrooms': ['exact'],
        }

class BookingFilter(django_filters.FilterSet):
    check_in_after = django_filters.DateFilter(field_name='check_in_date', lookup_expr='gte')
    check_in_before = django_filters.DateFilter(field_name='check_in_date', lookup_expr='lte')
    check_out_after = django_filters.DateFilter(field_name='check_out_date', lookup_expr='gte')
    check_out_before = django_filters.DateFilter(field_name='check_out_date', lookup_expr='lte')
    
    class Meta:
        model = Booking
        fields = {
            'status': ['exact'],
            'listing': ['exact'],
            'guest': ['exact'],
        }