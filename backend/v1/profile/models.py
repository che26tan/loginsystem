import random
import string
import uuid
import os
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from account.models import MyUser, VerificationStatus
from account.models import GenderType


def user_profile_image_upload_path(instance, filename):
    # Generate a unique image UUID and save it on the instance if not set
    if instance.profile_image:
        instance.image_uuid = uuid.uuid4()

    # Store under user_id and use UUID as filename
    ext = filename.split('.')[-1]
    return f"profile_images/{instance.user.user_id}/{instance.image_uuid}.{ext}"

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    allowed_ext = ['.jpg', '.jpeg', '.png', '.svg']
    if ext not in allowed_ext:
        raise ValidationError(f'Unsupported file extension: {ext}. Allowed: {allowed_ext}')

class Profile(models.Model):
    user = models.OneToOneField(MyUser, primary_key=True, on_delete=models.CASCADE, verbose_name="User Id")
    phone_number = models.CharField(
        verbose_name="Phone Number",
        max_length=10,
        null=True,
        blank=True,
        validators=[
            RegexValidator(regex=r'^\d{10}$', message="Phone number must be exactly 10 digits.")
        ]
    )
    is_phone_number_verified = models.BooleanField(
        verbose_name="Phone Verification Status",
        choices=VerificationStatus.STATUS,
        default=VerificationStatus.NOT_VERIFIED
    )
    address = models.CharField(verbose_name='Address', max_length=100, null=True, blank=True)
    city = models.CharField(verbose_name='City', max_length=100, null=True, blank=True)
    state = models.CharField(verbose_name='State', max_length=100, null=True, blank=True)
    postal_code = models.CharField(verbose_name='Postal Code', max_length=100, null=True, blank=True)
    profile_image = models.ImageField(verbose_name="User Profile Image", upload_to=user_profile_image_upload_path,
                                      validators=[validate_file_extension], null=True, blank=True)
    referral_id = models.CharField(max_length=12, unique=True, null=True, blank=True)
    referral_points = models.PositiveSmallIntegerField(verbose_name='Referral Points', default=0)

    def save(self, *args, **kwargs):
        if not self.profile_image:
            if self.user.gender == GenderType.male:
                self.profile_image = './media/profile_images/default/male.svg'
            elif self.user.gender == GenderType.female:
                self.profile_image = './media/profile_images/default/female.svg'
            else:  # If gender is something else (e.g., non-binary, not specified)
                self.profile_image = './media/profile_images/default/other.svg'

        if not self.referral_id:  # Generate referral ID only if not already set
            self.referral_id = self.referral_id_generator()

        super().save(*args, **kwargs)

    @staticmethod
    def referral_id_generator():
        while True:
            referral_id = ''.join(
                random.choices(string.ascii_letters + string.digits, k=10))  # Generates a 10-character long id
            if not Profile.objects.filter(referral_id=referral_id).exists():
                return referral_id

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username
