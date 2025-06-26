from rest_framework.routers import DefaultRouter
from django.urls import path, include
from profile import views

router = DefaultRouter()
router.register(r'', views.ProfileViewSet , basename='profile')

urlpatterns = [
    path('', include(router.urls), name='profile'),
    path('demo', views.demo, name='profile-demo'),
]