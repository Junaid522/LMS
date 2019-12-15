from django.urls import path

from .views import PasswordResetView, SignUp, getpage, saveimage

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('password/', PasswordResetView.as_view(), name='change_password'),
    path('password/<int:user_id>/reset/', PasswordResetView.as_view(), name='change_user_password'),
    path('getimage/', getpage, name='getpage'),
    path('save_image/', saveimage, name='save_image'),
    # path('save_image/', CaptureImageView.as_view(), name='save_image'),
]
