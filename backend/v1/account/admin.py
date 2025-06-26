from django.contrib import admin
from account.models import MyUser


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    search_fields = ['user_id', 'username',]
    list_display = ['created_at', 'user_id', 'username', 'email', 'is_email_verified', 'country_alpha_code', 'country_phone_code', 'country_name',
                'gender', 'dob', 'user_type', 'age', 'full_name']

