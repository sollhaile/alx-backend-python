from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.db.models import Q
from .models import Listing, Booking
from .serializers import (
    ListingSerializer, ListingCreateSerializer,
    BookingSerializer
)
from .filters import ListingFilter, BookingFilter

class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing property listings.
    
    Provides CRUD operations for listings with filtering, searching, and ordering capabilities.
    """
    queryset = Listing.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = ListingFilter
    search_fields = ['title', 'description', 'city', 'amenities']
    ordering_fields = ['created_at', 'price_per_night', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ListingCreateSerializer
        return ListingSerializer

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Listing.objects.all()
        
        # Filter by current user's listings if requested
        if self.action in ['update', 'partial_update', 'destroy']:
            queryset = queryset.filter(host=self.request.user)
        
        return queryset

    @extend_schema(
        summary="List all listings",
        description="Retrieve a paginated list of all active listings with filtering and search capabilities.",
        parameters=[
            OpenApiParameter(
                name='property_type',
                description='Filter by property type',
                required=False,
                type=str,
                examples=[
                    OpenApiExample('Apartment', value='apartment'),
                    OpenApiExample('House', value='house'),
                ]
            ),
            OpenApiParameter(
                name='min_price',
                description='Minimum price per night',
                required=False,
                type=OpenApiTypes.NUMBER,
            ),
            OpenApiParameter(
                name='max_price',
                description='Maximum price per night',
                required=False,
                type=OpenApiTypes.NUMBER,
            ),
            OpenApiParameter(
                name='city',
                description='Filter by city (case-insensitive partial match)',
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name='search',
                description='Search in title, description, city, and amenities',
                required=False,
                type=str,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new listing",
        description="Create a new property listing. The authenticated user becomes the host.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a specific listing",
        description="Get detailed information about a specific listing.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a listing",
        description="Update a listing. Only the host can update their own listings.",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a listing",
        description="Partially update a listing. Only the host can update their own listings.",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a listing",
        description="Delete a listing. Only the host can delete their own listings.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Get user's listings",
        description="Retrieve all listings belonging to the authenticated user.",
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_listings(self, request):
        """Get current user's listings"""
        listings = self.queryset.filter(host=request.user)
        page = self.paginate_queryset(listings)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(listings, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get listing availability",
        description="Check if a listing is available for specific dates.",
        parameters=[
            OpenApiParameter('check_in', OpenApiTypes.DATE, required=True),
            OpenApiParameter('check_out', OpenApiTypes.DATE, required=True),
        ]
    )
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Check listing availability for given dates"""
        listing = self.get_object()
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')
        
        if not check_in or not check_out:
            return Response(
                {'error': 'check_in and check_out dates are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            listing=listing,
            status__in=['confirmed', 'pending'],
            check_in_date__lt=check_out,
            check_out_date__gt=check_in
        )
        
        is_available = not overlapping_bookings.exists()
        
        return Response({
            'available': is_available,
            'conflicting_bookings': overlapping_bookings.count()
        })

class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings.
    
    Provides CRUD operations for bookings with filtering capabilities.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BookingFilter
    ordering_fields = ['created_at', 'check_in_date', 'check_out_date']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter bookings based on user role"""
        user = self.request.user
        
        # Users can see bookings where they are either the guest or the host
        return Booking.objects.filter(
            Q(guest=user) | Q(listing__host=user)
        )

    @extend_schema(
        summary="List user's bookings",
        description="Retrieve all bookings where the user is either the guest or the host of the listing.",
        parameters=[
            OpenApiParameter(
                name='status',
                description='Filter by booking status',
                required=False,
                type=str,
                examples=[
                    OpenApiExample('Pending', value='pending'),
                    OpenApiExample('Confirmed', value='confirmed'),
                    OpenApiExample('Cancelled', value='cancelled'),
                    OpenApiExample('Completed', value='completed'),
                ]
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new booking",
        description="Create a new booking for a listing. The user making the request becomes the guest.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a specific booking",
        description="Get detailed information about a specific booking.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a booking",
        description="Update a booking. Only the guest or host can update the booking.",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a booking",
        description="Partially update a booking. Only the guest or host can update the booking.",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Cancel a booking",
        description="Cancel a booking. Changes status to 'cancelled'.",
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        
        if booking.status == 'cancelled':
            return Response(
                {'error': 'Booking is already cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if booking.status == 'completed':
            return Response(
                {'error': 'Cannot cancel a completed booking'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @extend_schema(
        summary="Confirm a booking",
        description="Confirm a booking. Only the host can confirm bookings.",
    )
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a booking (host only)"""
        booking = self.get_object()
        
        # Only the host can confirm bookings
        if request.user != booking.listing.host:
            return Response(
                {'error': 'Only the listing host can confirm bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status != 'pending':
            return Response(
                {'error': 'Only pending bookings can be confirmed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'confirmed'
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)