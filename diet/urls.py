from django.urls import path

from .views import recommand

app_name = "diet"
urlpatterns = [
    path("recommand/", recommand, name="recommand_diet"),
]
