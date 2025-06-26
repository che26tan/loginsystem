from rest_framework.routers import DefaultRouter
from django.urls import path, include
from metadata import views

router = DefaultRouter()
router.register(r'metadata', views.MetaDataViewSet , basename='metadataviewset')

urlpatterns = [
    path('', include(router.urls), name='metadata'),
    path('demo', views.demo, name='metadata-demo'),
]