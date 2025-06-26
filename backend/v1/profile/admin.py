from django.contrib import admin
from profile.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user', 'address', 'city', 'state', 'postal_code', 'subscription']
    list_display = ['user', 'phone_number', 'is_phone_number_verified', 'address', 'city', 'state', 'postal_code',
                    'profile_image', 'referral_id', 'referral_points',
                    ]
