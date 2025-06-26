import base64
import pyotp
import jwt
from datetime import datetime, timedelta, UTC
from django.core.mail import send_mail
from django.core.cache import caches
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from common.utility.functions import standard_response
from account.models import MyUser
from account.serializers import UserSerializer, PasswordResetSerializer, PasswordChangeSerializer


MyUser = get_user_model()

def demo(request):
    return HttpResponse("account api is working")

class UserViewSet(viewsets.ViewSet):
    @action(methods=['POST'], url_path='signup', detail=False, permission_classes=[AllowAny])
    def auth_user_signup(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # validated_data = serializer.validated_data
            # print(validated_data)
            serializer.save()
            code=status.HTTP_201_CREATED
            # return standard_response(True,"signed up successfully", data=serializer.data, code=code)
            return standard_response(True, "signup successful", code=code)
        code=status.HTTP_400_BAD_REQUEST
        return standard_response(False,"signup failed",error=serializer.errors, code=code)

    @action(methods=['POST'], url_path='login', detail=False, permission_classes=[AllowAny])
    def auth_user_login(self, request):
        auth_header = request.headers.get('Authorization')
        # print(auth_header)

        if not auth_header or not auth_header.startswith('Basic '):
            return standard_response(
                success=False,
                message="login failed",
                error="auth header missing",
                code=status.HTTP_400_BAD_REQUEST
            )

        try:
            auth_data = auth_header.split(' ')[1]  # Extract Base64 part
            decoded_data = base64.b64decode(auth_data).decode('utf-8')  # Decode and convert to string
            username, password = decoded_data.split(':',1)  # Split into username and password
        except Exception:
            return standard_response(
                success=False,
                message="login failed",
                error="Invalid base64 or credentials format",
                code=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is None:
            try:
                MyUser.objects.get(username=username)
                return standard_response(False, "login failed", error='Incorrect Password', code=status.HTTP_401_UNAUTHORIZED)
            except MyUser.DoesNotExist:
                return standard_response(False, "login failed", error='user not found', code=status.HTTP_404_NOT_FOUND)
        else:
            refresh = RefreshToken.for_user(user)
            # return standard_response(True, "logged in successfully",data={
            #     'access': str(refresh.access_token),
            #     'refresh': str(refresh),
            #     'user_data': {
            #         'id': user.user_id,
            #         'username': user.username,
            #         'email': user.email,
            #     }}, code=status.HTTP_200_OK)
            return standard_response(True, "login successful", data={
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, code=status.HTTP_200_OK)


    @action(methods=['POST'], url_path='logout', detail=False, permission_classes=[IsAuthenticated])
    def auth_user_logout(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return standard_response(False, "logout failed", error='missing refresh token', code=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token) # To validate Refresh Token
            token.blacklist()
            return standard_response(True, "logout successful", code=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return standard_response(False, "logout failed", error='invalid token', code=status.HTTP_400_BAD_REQUEST)


    @action(methods=['PUT'], url_path='update', detail=False, permission_classes=[IsAuthenticated])
    def auth_user_update(self, request):
        user = request.user

        restricted_fields = ['password', 'username', 'email', 'created_at', 'user_id']
        for field in restricted_fields:
            if field in request.data:
                return standard_response(False,'update failed', error="This field cannot be updated.", code=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return standard_response(True, 'update successful', data=serializer.data,
                                     code=status.HTTP_200_OK)

        return standard_response(False,'update failed', error=serializer.errors, code=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], url_path='delete', detail=False, permission_classes=[IsAuthenticated])
    def auth_user_delete(self, request):
        user = request.user
        user.delete()
        return standard_response(True, 'delete successful', code=status.HTTP_204_NO_CONTENT)


class ConfirmViewSet(viewsets.ViewSet):
    @action(methods=['POST'], url_path='email', detail=False, permission_classes=[IsAuthenticated])
    def auth_confirm_email(self, request):
        user = request.user
        email = user.email
        username = user.username
        otp_entered = request.data.get('otp')

        otp_cache = caches['otp_cache']
        # Retrieve secret key from cache
        cached_data = otp_cache.get(f'evo_{email}_{username}')

        if not cached_data:
            return standard_response(False,'email confirm failed', error='OTP expired or not found', code=status.HTTP_400_BAD_REQUEST)

        # Validate OTP
        if cached_data['otp'] == otp_entered:
            return standard_response(True,'email confirm successful', data='OTP verified and Email Confirmed', code=status.HTTP_200_OK)
        else:
            return standard_response(False, 'email confirm failed', error='Invalid OTP',
                                     code=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], url_path='phone', detail=False, permission_classes=[IsAuthenticated])
    def auth_confirm_phone(self, request):
        user = request.user
        # if not user.is_authenticated:
        #     return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        phone = user.phone_number
        username = user.username
        otp_entered = request.data.get('otp')

        otp_cache = caches['otp_cache']
        # Retrieve secret key from cache
        cached_data = otp_cache.get(f'pvo_{phone}_{username}')

        if not cached_data:
            return standard_response(False,'phone confirm failed', error='OTP expired or not found', code=status.HTTP_400_BAD_REQUEST)

        # Validate OTP
        if cached_data['otp'] == otp_entered:
            # change status in db also***** ------------------------------------------------
            return standard_response(True,'phone confirm successful', data='OTP verified and Phone Confirmed', code=status.HTTP_200_OK)
        else:
            return standard_response(False, 'phone confirm failed', error='Invalid OTP', code=status.HTTP_400_BAD_REQUEST)


class VerifyViewSet(viewsets.ViewSet):
    @action(methods=['POST'], url_path='email', detail=False, permission_classes=[IsAuthenticated])
    def auth_verify_email(self, request):
        user = request.user
        # if not user.is_authenticated:
        #     return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate a unique secret key for this user
        email = user.email
        username = user.username
        secret_key = pyotp.random_base32()

        # Generate a Time-based OTP (TOTP)
        totp = pyotp.TOTP(secret_key)
        otp = totp.now()  # OTP valid for 30 seconds

        otp_cache = caches['otp_cache']
        # Store the secret key in cache for 5 minutes (300 sec)
        otp_cache.set(f'evo_{email}_{username}', {'secret_key': secret_key, 'otp': otp}, timeout=300)

        # Send OTP via email
        send_mail(
            'Password Reset OTP',
            f'Your OTP for password reset is {otp}. It will only valid for 5 minutes.',
            None,  # Change to your sender email
            [email],
            fail_silently=False,
        )

        return standard_response(True, 'email otp sent successful', code=status.HTTP_200_OK)

    @action(methods=['POST'], url_path='phone', detail=False, permission_classes=[IsAuthenticated])
    def auth_verify_phone(self, request):
        user = request.user
        # if not user.is_authenticated:
        #     return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate a unique secret key for this user
        phone = user.phone
        username = user.username
        secret_key = pyotp.random_base32()

        # Generate a Time-based OTP (TOTP)
        totp = pyotp.TOTP(secret_key)
        otp = totp.now()  # OTP valid for 30 seconds

        otp_cache = caches['otp_cache']
        # Store the secret key in cache for 5 minutes (300 sec)
        otp_cache.set(f'pvo_{phone}_{username}', {'secret_key': secret_key, 'otp': otp},
                      timeout=300)

        # Send OTP via phone
        #---------------------------------

        # send_mail(
        #     'Password Reset OTP',
        #     f'Your OTP for password reset is {otp}. It will only valid for 5 minutes.',
        #     None,  # Change to your sender email
        #     [email],
        #     fail_silently=False,
        # )

        return standard_response(True, 'phone otp sent successful', code=status.HTTP_200_OK)


class PasswordViewSet(viewsets.ViewSet):
    @action(methods=['POST'], url_path='forget', detail=False, permission_classes=[AllowAny])
    def auth_password_forget(self, request):
        email = request.data.get('email')
        username = request.data.get('username')

        try:
            user = MyUser.objects.get(username=username)
            if user.email != email:
                return standard_response(False, 'password forget failed', error='Invalid email',
                                         code=status.HTTP_400_BAD_REQUEST)
        except MyUser.DoesNotExist:
            return standard_response(False, 'password forget failed', error='Invalid username',
                                     code=status.HTTP_400_BAD_REQUEST)

        # Generate a unique secret key for this user
        secret_key = pyotp.random_base32()

        # Generate a Time-based OTP (TOTP)
        totp = pyotp.TOTP(secret_key)
        otp = totp.now()  # OTP valid for 30 seconds

        otp_cache = caches['otp_cache']
        # Store the secret key in cache for 30 minutes (1800 sec)
        # pro = password reset otp
        otp_cache.set(f'pro_{email}_{username}', {'secret_key': secret_key, 'otp': otp}, timeout=1800)

        # Send OTP via email
        send_mail(
            'Password Reset OTP',
            f'Your OTP for password reset is {otp}. It will only valid for 30 minutes.',
            None,  # Change to your sender email
            [email],
            fail_silently=False,
        )
        return standard_response(True, 'password forget successful', data='OTP sent to your email', code=status.HTTP_200_OK)

    @action(methods=['POST'], url_path='forget/confirm', detail=False, permission_classes=[AllowAny])
    def auth_password_forget_confirm(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        otp_entered = request.data.get('otp')

        otp_cache = caches['otp_cache']

        cached_data = otp_cache.get(f'pro_{email}_{username}')

        if not cached_data:
            return standard_response(False,'password forget confirm failed', error='OTP expired or not found', code=status.HTTP_400_BAD_REQUEST)

        # Validate OTP
        if cached_data['otp'] == otp_entered:
            return standard_response(True,'password forget confirm successful', data='OTP verified. You can reset your password', code=status.HTTP_200_OK)
        else:
            return standard_response(False, 'password forget confirm failed', error='Invalid OTP',
                                     code=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], url_path='reset', detail=False, permission_classes=[AllowAny])
    def auth_password_reset(self, request):
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            otp_entered = serializer.validated_data['otp']

            otp_cache = caches['otp_cache']
            cached_data = otp_cache.get(f'pro_{email}_{username}')

            if not cached_data:
                return standard_response(False,'password reset failed', error='OTP expired or not found', code=status.HTTP_400_BAD_REQUEST)

            # Validate OTP
            if cached_data['otp'] == otp_entered:
                serializer.save()
                otp_cache.delete(f'pro_{email}_{username}')
                return standard_response(True,'password reset successful', data='Password Changed', code=status.HTTP_200_OK)
            else:
                return standard_response(False,'password reset failed', error='Invalid OTP', code=status.HTTP_400_BAD_REQUEST)

        return standard_response(False, 'password reset failed', error=serializer.errors, code=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], url_path='change', detail=False, permission_classes=[IsAuthenticated])
    def auth_password_change(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return standard_response(True,'password change successful', code=status.HTTP_200_OK)
        return standard_response(False, 'password change failed', error=serializer.errors, code=status.HTTP_400_BAD_REQUEST)

class JWTViewSet(viewsets.ViewSet):
    @action(methods=['POST'], url_path='check', detail=False, permission_classes=[IsAuthenticated])
    def jwt(self,request):
        from rest_framework_simplejwt.tokens import AccessToken
        # token = request.auth
        # print(token)# Get JWT token from request
        # # if isinstance(token, AccessToken):
        # #     decoded_token = dict(token)  # Convert AccessToken to a dictionary
        # # else:
        # #     decoded_token = {"error": "Invalid token"}
        # #
        # # return Response({"decoded_jwt": decoded_token})
        # #
        user = request.user  # Extracted from JWT
        # print(user.__dict__)
        return standard_response(True, 'jwt successful', data={
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
        }, code=status.HTTP_200_OK)

    @action(methods=['POST'], url_path='get-access', detail=False, permission_classes=[AllowAny])
    def auth_jwt_access(self, request):
        try:
            refresh_token = request.data.get('refresh')
            refresh = RefreshToken(refresh_token)
            return standard_response(True,'jwt access successful',data={'access': str(refresh.access_token)}, code=status.HTTP_200_OK)
        except TokenError:
            return standard_response(False, 'jwt access failed', error="Invalid or expired refresh token",
                                     code=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], url_path='get-refresh', detail=False, permission_classes=[AllowAny])
    def auth_jwt_refresh(self, request):
        """Generate a new refresh token if the existing one is close to expiry."""
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return standard_response(False, 'jwt refresh failed', error="Refresh token is required",
                                         code=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken(refresh_token)

            # Decode the refresh token to check expiration
            decoded_token = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
            exp_timestamp = decoded_token.get("exp", 0)

            # Convert to aware datetime using settings timezone
            exp_time = datetime.fromtimestamp(exp_timestamp, tz=UTC)
            current_time = datetime.now(tz=UTC)

            # Calculate remaining time
            remaining_time = exp_time - current_time

            if remaining_time > timedelta(minutes=2):
                return standard_response(False,'jwt refresh failed',error="Refresh token is not close to expiration",
                                code=status.HTTP_425_TOO_EARLY)

            # Generate new refresh and access tokens
            user_id = refresh['user_id']
            user = MyUser.objects.get(user_id=user_id)
            new_refresh = RefreshToken.for_user(user)
            return standard_response(True,'jwt refresh successful',data=
                {
                    "refresh": str(new_refresh),
                    "access": str(new_refresh.access_token),
                },
                code=status.HTTP_200_OK,
            )
        except (TokenError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return standard_response(False, 'jwt refresh failed', error="Invalid or expired refresh token",
                                     code=status.HTTP_400_BAD_REQUEST)


class SecurityViewSet(viewsets.ViewSet):
    @action(methods=['POST'], url_path='2fa/setup', detail=False, permission_classes=[IsAuthenticated])
    def auth_secure_2fa_setup(self, request):
        return standard_response(True,'demo',code=status.HTTP_200_OK)