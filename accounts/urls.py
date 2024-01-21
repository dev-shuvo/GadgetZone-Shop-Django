from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("dashboard/", dashboard, name="dashboard"),
    path(
        "order-details/<int:order_number>/",
        order_details,
        name="order_details",
    ),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path(
        "password/validate/<uidb64>/<token>/",
        reset_password_validate,
        name="reset_password_validate",
    ),
    path("reset-password/", reset_password, name="reset_password"),
]
