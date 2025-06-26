import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from rest_framework import serializers
# from admin_panel.models import SubscriptionDetails
from profile.models import Profile
from account.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    country_name = serializers.CharField(source='user.country_name', read_only=True)

    class Meta:
        model = Profile
        depth = 1
        fields = ['user', 'phone_number', 'is_phone_number_verified', 'address', 'city','state', 'country_name',
                  'postal_code', 'referral_id', 'referral_points']
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)

        instance.save()
        return instance


class ProfileImage(serializers.ModelSerializer):
    class Meta:
        model = Profile
        depth = 1
        fields = ['profile_image']

    profile_image_file = serializers.FileField()

    def validate(self, data):
        profile_image = data.FILES.get('profile_image')
        if profile_image:
            data.profile_image = profile_image
            ext = os.path.splitext(self.profile_image.name)[-1].lower()
            if ext not in ['.jpg', '.jpeg']:  # If not already JPEG
                try:
                    img = Image.open(self.profile_image)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")

                    buffer = BytesIO()
                    img.save(buffer, format='JPEG')
                    buffer.seek(0)

                    # Rename file using UUID and override the uploaded one
                    filename = f"{self.image_uuid}.jpg"
                    self.profile_image.save(filename, ContentFile(buffer.read()), save=False)
                except Exception as e:
                    print(f"Image conversion failed: {e}")

    def update(self, instance, validated_data):

        profile_image = validated_data.get('profile_image', instance.profile_image)


        instance.save()