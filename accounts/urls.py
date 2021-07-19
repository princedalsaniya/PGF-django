from django.urls import path
from .views import *
from django.contrib.auth import views as av

urlpatterns = [
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('signup/', signup, name="signup"),
    path('verfiyEmail/<uidb64>/<token>', verfy_email, name="verfiyEmail"),
    path('test/', getNextPID_tenant, name="test"),

    #Setting Profiles
    path('set_tenant/', set_tenant, name="set_tenant"),

    #Password Changing.
    path('password_change/',av.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/',av.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #Password Resetting.
    path('password_reset/', av.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', av.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', av.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', av.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]