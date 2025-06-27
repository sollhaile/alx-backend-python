#!/usr/bin/env python3
"""Seeder command to populate listings."""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing
from faker import Faker
import random

User = get_user_model()
faker = Faker()

class Command(BaseCommand):
    help = "Seed the database with sample listings"

    def handle(self, *args, **kwargs):
        # Create a default user
        user, created = User.objects.get_or_create(username="demo_user")
        if created:
            user.set_password("demo1234")
            user.email = "demo@example.com"
            user.save()

        for _ in range(10):
            Listing.objects.create(
                title=faker.sentence(nb_words=4),
                description=faker.paragraph(),
                price_per_night=round(random.uniform(30, 200), 2),
                owner=user,
                location=faker.city()
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded listings."))
