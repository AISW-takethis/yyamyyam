from django.urls import path

from .views import (
    recommend,
    record_list,
    record_add,
    record_edit,
    record_detail,
    record_detail_search,
    loading,
    my_page,
)

app_name = "diet"
urlpatterns = [
    path("recommend/", recommend, name="recommend_diet"),
    path("list", record_list, name="record_list"),
    path("add", record_add, name="record_add"),
    path("edit/<int:record_id>", record_edit, name="record_edit"),
    path("detail", record_detail, name="record_detail"),
    path("detail_search", record_detail_search, name="record_detail_search"),
    path("loading", loading, name="loading"),
    path("myPage", my_page, name="my_page"),
]
