from django.urls import path

from .views import recommand, record_list, record_add

app_name = "diet"
urlpatterns = [
    path("recommand/", recommand, name="recommand_diet"),
    path("list", record_list, name="record_list"),
    path("add", record_add, name="record_add"),
]
