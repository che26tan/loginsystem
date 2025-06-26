from django.urls import include, path
from rest_framework.routers import DefaultRouter
from admin_panel import views

router = DefaultRouter()
router.register('', views.OfferCodeViewSet, basename='offer_code')


urlpatterns = [
    path('', include(router.urls), name='admin-panel'),
    path('demo', views.demo, name='admin-panel-demo')
]