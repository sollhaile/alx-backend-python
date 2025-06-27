from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']

class ListingSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    amenities_list = serializers.ReadOnlyField()
    bookings_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'property_type', 'price_per_night',
            'bedrooms', 'bathrooms', 'max_guests', 'address', 'city', 'state',
            'country', 'postal_code', 'latitude', 'longitude', 'amenities',
            'amenities_list', 'house_rules', 'status', 'host', 'created_at',
            'updated_at', 'image', 'bookings_count'
        ]
        read_only_fields = ['id', 'host', 'created_at', 'updated_at', 'bookings_count']

    def get_bookings_count(self, obj):
        return obj.bookings.filter(status__in=['confirmed', 'completed']).count()

    def validate_price_per_night(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price per night must be greater than 0.")
        return value

    def validate_max_guests(self, value):
        if value <= 0:
            raise serializers.ValidationError("Maximum guests must be at least 1.")
        return value

class ListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'property_type', 'price_per_night',
            'bedrooms', 'bathrooms', 'max_guests', 'address', 'city', 'state',
            'country', 'postal_code', 'latitude', 'longitude', 'amenities',
            'house_rules', 'status', 'image'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['host'] = request.user
        return super().create(validated_data)

class BookingSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)
    guest = UserSerializer(read_only=True)
    duration_days = serializers.ReadOnlyField()
    listing_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_id', 'guest', 'check_in_date', 'check_out_date',
            'guests_count', 'total_price', 'status', 'special_requests',
            'created_at', 'updated_at', 'duration_days'
        ]
        read_only_fields = ['id', 'guest', 'total_price', 'created_at', 'updated_at']

    def validate(self, data):
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        
        if check_in and check_out:
            if check_in >= check_out:
                raise serializers.ValidationError("Check-out date must be after check-in date.")
            
            if check_in < timezone.now().date():
                raise serializers.ValidationError("Check-in date cannot be in the past.")
        
        # Validate guests count against listing capacity
        listing_id = data.get('listing_id')
        guests_count = data.get('guests_count')
        
        if listing_id and guests_count:
            try:
                listing = Listing.objects.get(id=listing_id)
                if guests_count > listing.max_guests:
                    raise serializers.ValidationError(
                        f"Number of guests ({guests_count}) exceeds listing capacity ({listing.max_guests})."
                    )
            except Listing.DoesNotExist:
                raise serializers.ValidationError("Invalid listing ID.")
        
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        listing_id = validated_data.pop('listing_id')
        listing = Listing.objects.get(id=listing_id)
        
        # Calculate total price
        check_in = validated_data['check_in_date']
        check_out = validated_data['check_out_date']
        duration = (check_out - check_in).days
        total_price = listing.price_per_night * duration
        
        validated_data['guest'] = request.user
        validated_data['listing'] = listing
        validated_data['total_price'] = total_price
        
        return super().create(validated_data)