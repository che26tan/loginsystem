import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.cache import caches
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError


# choices
class UserType(models.IntegerChoices):
    other = 0, 'Other'
    internal = 1, 'Employee'
    external = 2, 'Customer'


class VerificationStatus:
    VERIFIED = True
    NOT_VERIFIED = False
    STATUS = [
        (VERIFIED, 'Verified'),
        (NOT_VERIFIED, 'Not Verified'),
    ]


class GenderType(models.IntegerChoices):
    male = 0, 'Male'
    female = 1 , 'Female'
    other = 2, 'Other'


# Models
class MyUser(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    username = models.CharField(verbose_name="Username", unique=True, max_length=100)
    email = models.EmailField(verbose_name="Email Address", unique=True)
    is_email_verified = models.BooleanField(
        verbose_name="Email Verification Status",
        choices=VerificationStatus.STATUS,
        default=VerificationStatus.NOT_VERIFIED
    )
    country_alpha_code = models.CharField(verbose_name="Country Alpha Code", max_length=5, null=True, blank=True)
    country_phone_code = models.PositiveSmallIntegerField(verbose_name="Country Phone Code", null=True, blank=True)
    country_name = models.CharField(verbose_name="Country Name", max_length=100, default="")
    gender = models.PositiveSmallIntegerField(verbose_name="Gender", choices=GenderType.choices, default=GenderType.other)
    dob = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    user_type = models.PositiveSmallIntegerField(verbose_name="User Type", choices=UserType.choices, default=UserType.external)
    age = models.PositiveIntegerField(verbose_name="Age", null=True, blank=True)
    full_name = models.CharField(verbose_name="Full Name", max_length=100)

    def cal_age(self):
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return None

    # Custom check when data is coming frontend and frontend is fetching same data from ecommerce
    def clean(self):
        """Validate country details before saving"""

        # If all fields are empty, set default and skip validation
        if not self.country_name and not self.country_phone_code and not self.country_alpha_code:
            self.country_name = "INDIA"
            self.country_phone_code = "91"
            self.country_alpha_code = "IN"
            return  # skip validation

        # Validation logic starts here if any field is provided
        cached_data = caches["metadata"]
        if not cached_data:
            raise ValidationError("Country data not found in cache2. Try again later.")

        country_data = cached_data.get("countries_data")
        if not country_data:
            raise ValidationError("Country data not found in cache. Try again later.")

        valid_country = any(
            country_a_code == str(self.country_alpha_code) and
            country_details["name"] == str(self.country_name) and
            country_details["phone_code"] == str(self.country_phone_code)
            for country_a_code, country_details in country_data.items()
        )

        if not valid_country:
            raise ValidationError(
                "Invalid country_name, country_phone_code, or country_alpha_code. Please select a valid country."
            )

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # True only if this is a new object

        if is_new:
            self.age = self.cal_age()
            self.full_name = self.get_full_name()
            self.clean()  # run validation ONLY on create
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "My User"
        verbose_name_plural = "My Users"

    def __str__(self):
        return self.username
