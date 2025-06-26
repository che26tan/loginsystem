from rest_framework.routers import DefaultRouter
from django.urls import path, include
from account import views

router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='auth_user')
router.register(r'confirm', views.ConfirmViewSet, basename='auth_confirm')
router.register(r'verify', views.VerifyViewSet, basename='auth_verify')
router.register(r'password', views.PasswordViewSet, basename='auth_password')
router.register(r'jwt', views.JWTViewSet, basename='auth_jwt')
router.register(r'secure', views.SecurityViewSet, basename='auth_security')


urlpatterns = [
    path('', include(router.urls), name='auth'),
    path('demo', views.demo, name='auth-demo'),
]
