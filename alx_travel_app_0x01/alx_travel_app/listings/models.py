#!/usr/bin/env python3
"""Models for listings app."""

from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Listing(models.Model):from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Listing(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('condo', 'Condominium'),
        ('villa', 'Villa'),
        ('studio', 'Studio'),
        ('loft', 'Loft'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    price_per_night = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    bedrooms = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    bathrooms = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    max_guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    amenities = models.TextField(help_text="Comma-separated list of amenities")
    house_rules = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='listings/', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['city', 'status']),
            models.Index(fields=['property_type', 'status']),
            models.Index(fields=['price_per_night']),
        ]

    def __str__(self):
        return f"{self.title} - {self.city}"

    @property
    def amenities_list(self):
        return [amenity.strip() for amenity in self.amenities.split(',') if amenity.strip()]

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['listing', 'status']),
            models.Index(fields=['guest', 'status']),
            models.Index(fields=['check_in_date', 'check_out_date']),
        ]

    def __str__(self):
        return f"Booking {self.id} - {self.listing.title}"

    def clean(self):
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        
        if self.check_in_date and self.check_out_date:
            if self.check_in_date >= self.check_out_date:
                raise ValidationError("Check-out date must be after check-in date.")
            
            if self.check_in_date < timezone.now().date():
                raise ValidationError("Check-in date cannot be in the past.")

    @property
    def duration_days(self):
        return (self.check_out_date - self.check_in_date).days

    """
    Represents a rental listing.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Booking(models.Model):
    """
    Represents a booking for a listing.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Booking by {self.user} for {self.listing}"

class Review(models.Model):
    """
    Represents a review for a listing.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user} for {self.listing}"
