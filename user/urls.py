from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("/", views.agreement, name="agreement"),
    path("signup/agreement/age", views.age, name="age"),
    path("signup/agreement/tos", views.tos, name="tos"),
    path("signup/agreement/pp", views.pp, name="pp"),
    path("signup/agreement/mc", views.mc, name="mc"),
]
