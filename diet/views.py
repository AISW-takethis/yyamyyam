from django.shortcuts import render

from django.contrib.auth.models import User
from user.models import UserProfile
from .models import Food

# for test
CALORIE_LIMIT = 2000
MORNING = 1000
LUNCH = 500
DINNER = 0

# Create your views here.
def recommend(request):
    # 잔여 칼로리
    remaining_calorie = CALORIE_LIMIT - MORNING - LUNCH - DINNER

    # 잔여 칼로리 이하의 음식 리스트, 랜덤 정렬해서 상위 3개 추출
    food_list = Food.objects.filter(
        calorie__lte=remaining_calorie, is_main=True
    ).order_by("?")[:3]

    # food의 name, description, image_path, calorie, carbohydrate, protein, fat 정보를 추출해서 프린트
    for food in food_list:
        food.calorie = int(round(food.calorie, 0))

    return render(request, "diet/recommend.html", {"food_list": food_list})


def record_list(request):
    return render(request, "diet/record_list.html", {})


def record_add(request):
    return render(request, "diet/record_add.html", {})


def record_detail(request):
    return render(request, "diet/record_detail.html", {})


# record_add 페이지를 공유해서 쓰되 전달하는 인자에 차이를 둔다.
def record_edit(request):
    return render(request, "diet/record_add.html", {})


def record_detail_search(request):
    item_list = [i for i in range(1, 11)]
    return render(request, "diet/record_detail_search.html", {"item_list": item_list})


def loading(request):
    return render(request, "loading.html", {})


def my_page(request):
    context = {
        "nickname": UserProfile.objects.get(user_id = request.user).nickname,
        "email": User.objects.filter(id = request.user.id).first().email,
    }
    
    return render(request, "diet/my_page.html", context)
