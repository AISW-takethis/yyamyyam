from django.urls import path

from .views import recommand

urlpatterns = [
    path("recommand/", recommand, name="recommand_diet"),
]
