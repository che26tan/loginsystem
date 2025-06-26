from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('account.urls'), name='auth-redirect'),
    path('admin-panel/', include('admin_panel.urls'), name='admin-panel-redirect'),
    path('profile/', include('profile.urls'), name='profile-redirect'),
    path('other/', include('metadata.urls'), name='metadata-redirect'),
]
