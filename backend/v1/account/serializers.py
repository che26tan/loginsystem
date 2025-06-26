from account.models import MyUser
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError
import re

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = MyUser
        fields = [
            'created_at', 'user_id', 'username', 'first_name', 'last_name', 'email', 'password', 'password2', 'country_alpha_code', 'country_phone_code',
            'country_name', 'gender', 'dob', 'full_name', 'is_email_verified',
        ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'user_id': {'read_only': True},
            'password': {'style': {'input_type': 'password'}, 'min_length': 8, 'write_only': True},
            'email': {'required': True,},  # Email cannot be updated
            'username': {'required': True,},  # Username cannot be updated
            'full_name': {'required': False, 'allow_blank': True},
        }

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({'password2': 'Passwords must match'})

        if self.instance is None:
            if MyUser.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError({'email': 'This email is already registered.'})

            if MyUser.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError({'username': 'This username is already taken.'})

        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 as it's not in the model
        user = MyUser(**validated_data)
        user.set_password(validated_data['password'])  # Hash password
        user.save()
        return user

    def update(self, instance, validated_data):
        restricted_fields = ['password', 'username', 'email', 'created_at', 'user_id']

        for field in restricted_fields:
            validated_data.pop(field, None)

        # print(validated_data.items())

        for attr, value in validated_data.items():
            if attr not in restricted_fields:
                setattr(instance, attr, value)

        instance.save()
        return instance


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    otp = serializers.CharField(max_length=6, min_length=6)
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        """Custom validation for new password"""

        # Ensure password has at least one letter and one number
        if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain both letters and numbers.")

        # Validate password using Django’s built-in validator (checks for common passwords, complexity, etc.)
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    def validate(self, data):
        """Check if new_password and confirm_password match"""
        if data.get('password1') != data.get('password2'):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def save(self):
        """Save the new password in the database"""
        email = self.validated_data['email']
        username = self.validated_data['username']
        new_password = self.validated_data['password1']

        user = MyUser.objects.get(email=email, username=username)
        user.set_password(new_password)  # Hashes and saves the password
        user.save()


class PasswordChangeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()

    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

        # Step 1: Check if passwords match
        if password1 != password2:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        # Step 2: Fetch user and check new password != old password
        try:
            user = MyUser.objects.get(email=email, username=username)
        except MyUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        if user.check_password(password1):
            raise serializers.ValidationError({"new_password": "New password cannot be the same as the old password."})

        # Temporarily attach user instance for later use in save()
        self.user = user

        return data

    def validate_new_password(self, value):
        # Step 3: Check for complexity - must contain at least one letter and one number
        if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain both letters and numbers.")

        # Use Django’s built-in password validators
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    def save(self):
        new_password = self.validated_data['password1']
        user = self.user  # Retrieved and stored during `validate`
        user.set_password(new_password)
        user.save()