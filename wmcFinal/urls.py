from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('admin/', admin.site.urls),
    path('acc/', include('accounts.urls')),
    path('tenant/', include('tenant.urls')),
#     path('owner/', include('owner.urls')),
]