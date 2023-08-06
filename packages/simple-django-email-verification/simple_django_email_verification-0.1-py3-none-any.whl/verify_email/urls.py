from django.urls import path
from . import views

urlpatterns = [
    path(f'user/verify-email/<useremail>/<usertoken>/', views.verify_user_and_activate, name='verify-email'),
    path(f'user/verify-email/request-new-link/<useremail>/<usertoken>/', views.RequestNewLink.as_view(), name='request-new-link-from-token'),
    path(f'user/verify-email/request-new-link/', views.RequestNewLink.as_view(), name='request-new-link-from-email'),
]
