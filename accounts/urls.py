from django.urls import path

from .views import PasswordResetView, SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('password/', PasswordResetView.as_view(), name='change_password'),
    path('password/<int:user_id>/reset/', PasswordResetView.as_view(), name='change_user_password'),
]
