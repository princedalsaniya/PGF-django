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
    path('pg_list/', o_pglist, name="o_pglist"),
    path('pg_details/<str:pgID>/', pg_details, name="pg_details"),
    path('edit_pgDetails/', edit_pgDetails, name="edit_pgDetails"),
    path('edit_pgFacilities/', edit_pgFacilities, name="edit_pgFacilities"),
    path('edit_pgRules/', edit_pgRules, name="edit_pgRules"),
    path('delete_photo/<path:photoPID>/', delete_photo, name="delete_photo"),
    path('upload_new_photo', upload_new_photo, name="upload_new_photo"),
]
