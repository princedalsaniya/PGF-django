from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', o_dashboard, name="o_dashboard"),
    path('register_pg_details/', o_register_pg_details, name="o_register_pg_details"),
    path('register_facilities/', o_register_facilities, name="o_register_facilities"),
    path('register_rules/', o_register_rules, name="o_register_rules"),
    path('register_photos/', o_register_pg_photos, name="o_register_pg_photos"),
    path('upload_photo/', o_upload_pic, name="o_upload_pic"),
    path('register_success/', o_register_success, name="o_register_success"),
]
