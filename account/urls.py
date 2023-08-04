from django.urls import include, path

from .views import JWTSignInView, SignupView

urlpatterns = [
    path("register/", SignupView.as_view(), name="register"),
    path("token/", JWTSignInView.as_view(), name="login"),
]
