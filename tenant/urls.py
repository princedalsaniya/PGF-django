from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', t_dashboard, name="t_dashboard"),
]
