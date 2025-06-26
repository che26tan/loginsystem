import uuid
from datetime import timedelta
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class AdminPanel(models.Model):
    # pass

    class Meta:
        verbose_name = "Admin Panel"
        verbose_name_plural = "Admin Panel"

    # def __str__(self):
    #     return self.username

class OfferCode(models.Model):
    # Integer choices to prevent invalid values
    DAYS = 1
    MONTHS = 2
    YEARS = 3

    UNIT_CHOICES = [
        (DAYS, 'Days'),
        (MONTHS, 'Months'),
        (YEARS, 'Years'),
    ]

    code_id = models.AutoField(primary_key=True)
    code_name = models.CharField(verbose_name='Code Name', max_length=10, unique=True)
    value = models.PositiveIntegerField(verbose_name='Value in Percentage', validators=[MinValueValidator(1), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    expire_value = models.PositiveIntegerField(verbose_name="Expire Value", default=10, validators=[MinValueValidator(1)])
    expire_unit = models.PositiveSmallIntegerField(verbose_name="Expire Unit", choices=UNIT_CHOICES, default=DAYS)
    validation_date = models.DateTimeField(verbose_name="Validation Date", blank=True, null=True)
    valid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Calculate `validation_date` based on `expire_value` and `expire_unit`."""
        if not self.validation_date:  # Only set at creation
            if self.expire_unit == self.DAYS:
                self.validation_date = now() + timedelta(days=self.expire_value)
            elif self.expire_unit == self.MONTHS:
                self.validation_date = now() + timedelta(days=self.expire_value * 30)  # Approx. a month as 30 days
            elif self.expire_unit == self.YEARS:
                self.validation_date = now() + timedelta(days=self.expire_value * 365)  # Approx. a year as 365 days
        super().save(*args, **kwargs)

    @property
    def is_offer_valid(self):
        """Returns True if the offer is still valid, False otherwise."""
        return self.validation_date and self.validation_date > now()


    class Meta:
        verbose_name = "OfferCode"
        verbose_name_plural = "OfferCodes"

    def __str__(self):
        return self.code_name
