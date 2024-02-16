from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("signup/agreement/", views.agreement, name="agreement"),
    path("signup/agreement/age", views.age, name="age"),
    path("signup/agreement/tos", views.tos, name="tos"),
    path("signup/agreement/pp", views.pp, name="pp"),
    path("signup/agreement/mc", views.mc, name="mc"),
    path("signup/info/welcome", views.welcome, name="welcome"),
    path("signup/info/nickname", views.nickname, name="nickname"),
    path("signup/info/birth", views.birth, name="birth"),
    path("signup/info/physical", views.physical, name="physical"),
    path("signup/info/activity", views.activity, name="activity"),
    path("signup/info/kcal", views.kcal, name="kcal"),
    path("signup/complete", views.complete, name="complete"),
]
