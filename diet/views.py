import base64
from datetime import datetime
import json
import os

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.files.base import ContentFile

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
        food.carbohydrate = round(food.carbohydrate, 1)
        food.protein = round(food.protein, 1)
        food.fat = round(food.fat, 1)

    return render(request, "diet/recommend.html", {"food_list": food_list})


def record_list(request):
    return render(request, "diet/record_list.html", {})


def image_process(request):
    if request.method == "POST":
        date = datetime.now()
        time = date.strftime("%Y%m%d%H%M%S")

        data = json.loads(request.body.decode("utf-8"))
        image_data = data["image"]

        # 'data:image/png;base64,' 부분 제거
        format, imgstr = image_data.split(";base64,")
        ext = format.split("/")[-1]  # 이미지 확장차 추출

        # Base64 디코딩
        image_bytes = base64.b64decode(imgstr)

        image_file_name = time + "image." + ext
        file_path = os.path.join("static", "asset", "user_food", image_file_name)

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        return JsonResponse({"message": "success"}, status=200)
    return JsonResponse({"message": "fail"}, status=400)


def record_add(request):
    # 직접 입력하는거 구현하기

    return render(request, "diet/record_add.html", {})


def record_add_with_recommend(request, food_id):
    # 추천으로 넣는거 구현
    food = get_object_or_404(Food, id=food_id)

    # 현재 시간
    now = datetime.now()

    # 현재 날짜 추출
    date = now.strftime("%Y.%m.%d")
    # 현재 시간 오전/오후 추출
    ampm = now.strftime("%p")

    # 현재 시간 12시간제 추출
    time = now.strftime("%I:%M")

    # 시간 전처리
    if ampm == "AM":
        ampm = "오전"
    else:
        ampm = "오후"
    time = ampm + " " + time

    # 현재 시간을 기준으로 아침, 점심, 저녁 구분
    if now.hour < 10:
        meal_type = "breakfast"
    elif now.hour < 15:
        meal_type = "lunch"
    else:
        meal_type = "dinner"

    # food 전처리
    food.calorie = int(round(food.calorie, 0))
    food.carbohydrate = round(food.carbohydrate, 1)
    food.protein = round(food.protein, 1)
    food.fat = round(food.fat, 1)

    return render(
        request,
        "diet/record_add.html",
        {
            "food": food,
            "record_date": date,
            "record_time": time,
            "meal_type": meal_type,
        },
    )


# record_add 페이지를 공유해서 쓰되 전달하는 인자에 차이를 둔다.
def record_edit(request, record_id):
    return render(request, "diet/record_add.html", {})


def record_detail(request):
    return render(request, "diet/record_detail.html", {})


def record_detail_search(request):
    item_list = [i for i in range(1, 11)]
    return render(request, "diet/record_detail_search.html", {"item_list": item_list})


def search_items(request, term):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        query = term  # 'term'은 검색어 파라미터의 이름
        items = Food.objects.filter(
            name__icontains=query
        )  # 'name' 필드를 검색어로 필터링, 실제 모델의 필드에 맞게 수정
        food_dict = {}
        for item in items:
            food_dict[item.id] = {
                "name": item.name,
                "calorie": item.calorie,
                "carbohydrate": item.carbohydrate,
                "protein": item.protein,
                "fat": item.fat,
            }

        return JsonResponse(food_dict, safe=False)
    return JsonResponse({"error": "Not Ajax request"}, status=400)


def loading(request):
    return render(request, "loading.html", {})


def my_page(request):
    context = {
        "nickname": UserProfile.objects.get(user_id = request.user).nickname,
        "email": User.objects.filter(id = request.user.id).first().email,
    }
    
    return render(request, "diet/my_page.html", context)
