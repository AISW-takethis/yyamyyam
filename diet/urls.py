from django.urls import path

from .views import (
    recommend,
    record_list,
    record_add,
    record_add_with_recommend,
    record_edit,
    record_detail,
    record_detail_search,
    loading,
    my_page,
    image_process,
    search_items,
)


def get_date_string():
    from datetime import datetime

    now = datetime.now()
    return now.strftime("%Y-%m-%d")


now = get_date_string()

app_name = "diet"
urlpatterns = [
    path("recommend/", recommend, name="recommend_diet"),
    path("list/", record_list, name="record_list_empty"),
    path(f"list/?date={now}", record_list, name="record_list"),
    path("image_process", image_process, name="image_process"),
    path("add/", record_add, name="record_add"),
    path(
        "add/<int:food_id>", record_add_with_recommend, name="record_add_with_recommend"
    ),
    path("edit/<int:record_id>", record_edit, name="record_edit"),
    path("detail/", record_detail, name="record_detail"),
    path("detail_search/", record_detail_search, name="record_detail_search"),
    path("search_items/<str:term>", search_items, name="search_items"),
    path("loading", loading, name="loading"),
    path("mypage/", my_page, name="my_page"),
]
