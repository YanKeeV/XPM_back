from django.urls import path
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm


from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, SetImageAPIView
)

app_name = 'core'
urlpatterns = [
    path('user', UserRetrieveUpdateAPIView.as_view()),
    path('user/registration/', RegistrationAPIView.as_view()),
    path('user/login/', LoginAPIView.as_view()),
    path('user/set-image/', SetImageAPIView.as_view()),

    path('user/password_reset/', reset_password_request_token, name='reset-password-request'),
    path('user/password_reset/confirm/', reset_password_confirm, name='reset-password-confirm'),
]