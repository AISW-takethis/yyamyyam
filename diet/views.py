import base64
from datetime import datetime
import json
import os

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.files.base import ContentFile

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils import timezone

from user.models import UserProfile
from .models import Food, UserDiet, DetailOfDiet


# for test
CALORIE_LIMIT = 2000
MORNING = 1000
LUNCH = 500
DINNER = 0


def record_date_mealtype():
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

    return now, date, time, meal_type


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
    date = request.GET.get("date", datetime.now().strftime("%Y-%m-%d"))

    # data 조희
    diet_data = UserDiet.objects.filter(take_date=date, user_id=request.user.id)
    user_calorie = UserProfile.objects.get(
        user_id=request.user.id
    ).recommend_daily_calorie

    diet_list = []
    diet_detail_list = []

    day_calorie = 0
    day_carbohydrate = 0
    day_protein = 0
    day_fat = 0

    for diet in diet_data:
        diet_detail_data = DetailOfDiet.objects.filter(diet_id=diet.id)

        diet_calorie = 0
        diet_carbohydrate = 0
        diet_protein = 0
        diet_fat = 0

        for detail in diet_detail_data:
            diet_detail_list.append(
                [
                    diet.id,
                    detail.id,
                    detail.name,
                    detail.carbohydrate,
                    detail.protein,
                    detail.fat,
                    detail.calorie,
                    detail.quantity,
                    detail.image_path,
                ]
            )

            diet_calorie += detail.calorie
            diet_carbohydrate += detail.carbohydrate
            diet_protein += detail.protein
            diet_fat += detail.fat

        day_calorie += diet_calorie
        day_carbohydrate += diet_carbohydrate
        day_protein += diet_protein
        day_fat += diet_fat

        # meal: 1: 아침, 2: 점심, 3: 저녁, 4:간식, 5: 야식
        meal = ""
        if diet.meal == 1:
            meal = "아침"
            selected_option = "breakfast"
        elif diet.meal == 2:
            meal = "점심"
            selected_option = "lunch"
        elif diet.meal == 3:
            meal = "저녁"
            selected_option = "dinner"
        elif diet.meal == 4:
            meal = "간식"
            selected_option = "snack"
        elif diet.meal == 5:
            meal = "야식"
            selected_option = "night"

        # text-date와 text-time을 만들자.
        # text-date는 2021.10.10 형식으로 만들자.
        text_date = diet.take_at.strftime("%Y.%m.%d")
        # text-time은 오전 10:00 형식으로 만들자.
        text_time = diet.take_at.strftime("%p %I:%M")

        if "AM" in text_time:
            text_time = text_time.replace("AM", "오전")
        else:
            text_time = text_time.replace("PM", "오후")

        diet_list.append(
            (
                diet.id,
                {
                    "take_at": diet.take_at,
                    "take_date": diet.take_date,
                    "meal": meal,
                    "selected_option": selected_option,
                    "image_path": diet.image_path,
                    "memo": diet.memo,
                    "total_calorie": int(diet_calorie),
                    "total_carbohydrate": int(diet_carbohydrate),
                    "total_protein": int(diet_protein),
                    "total_fat": int(diet_fat),
                    "text_date": text_date,
                    "text_time": text_time,
                },
            )
        )

    # 섭취 순서로 정렬
    diet_list = sorted(diet_list, key=lambda x: x[1]["take_at"])
    return render(
        request,
        "diet/record_list.html",
        {
            "date": date,
            "diet_list": diet_list,
            "detail_list": diet_detail_list,
            "day_calorie": int(day_calorie),
            "day_carbohydrate": int(day_carbohydrate),
            "day_protein": int(day_protein),
            "day_fat": int(day_fat),
            "user_calorie": user_calorie,
        },
    )


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
        file_path = os.path.join("static", "media", "user_food", image_file_name)

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        return JsonResponse({"message": "image upload success"}, status=200)
    return JsonResponse({"message": "fail"}, status=400)


def save_image(image64, image_file_path):
    if image64:
        # 'data:image/png;base64,' 부분 제거
        format, imgstr = image64.split(";base64,")
        # ext = format.split("/")[-1]  # 이미지 확장차 추출

        # Base64 디코딩
        image_bytes = base64.b64decode(imgstr)

        with open(image_file_path, "wb") as f:
            f.write(image_bytes)
        return True
    return False


def convert_string_to_datetime(date_string):
    # 오전/오후를 AM/PM으로 변환
    if "오전" in date_string:
        date_string = date_string.replace("오전", "AM")
    elif "오후" in date_string:
        date_string = date_string.replace("오후", "PM")

    # datetime 객체로 변환

    date_format = "%Y년 %m월 %d일 %I:%M %p"
    try:
        result = datetime.strptime(date_string, date_format)
    except ValueError:
        date_format = "%Y년 %m월 %d일 %p %I:%M"
        result = datetime.strptime(date_string, date_format)
    result = timezone.make_aware(result, timezone.get_default_timezone())
    return result


# 여기서 날자 시간//메인이미지//식사 종류//음식-->디테일로//메모 뽑아서 DB에 저장
# 이미지 이름 규칙은 아이디.jpeg
@csrf_exempt
def record_add(request):
    if request.method == "POST":
        data = request.POST
        save_datetime = timezone.make_aware(
            datetime.now(), timezone.get_default_timezone()
        )
        string_save_datetime = save_datetime.strftime("%Y%m%d%H%M%S")
        image_file_name = str(request.user.id) + str(string_save_datetime) + ".jpeg"
        diet_image_file_path = os.path.join(
            "static", "media", "user_food", image_file_name
        )

        # 이미지 저장
        if not save_image(data["imageBase64"], diet_image_file_path):
            diet_image_file_path = "static/media/user_food/default.jpeg"
        # #
        # # # (완료) 식단 기록 ############################################################
        # # 식단 기록
        diet = UserDiet()

        datetime_list = data["take_at"].strip().split()

        # test

        date_list = [int(i[:-1]) for i in datetime_list[:3]]

        print(date_list)

        diet.take_at = convert_string_to_datetime(data["take_at"])
        diet.take_date = datetime(*date_list).date()
        diet.meal = data["meal"]  # 1: 아침, 2: 점심, 3: 저녁, 4:간식, 5: 야식
        diet.image_path = diet_image_file_path  # 이미지 경로.
        diet.memo = data["meal_memo"]  # 식사 메모
        diet.created_at = save_datetime  # 생성 시간
        diet.updated_at = save_datetime  # 수정 시간
        diet.user_id = request.user.id  # 유저 아이디
        diet.save()
        #
        # # ### 디테일 ================================================================
        detail_of_diet = {}
        detail_of_diet_ids = []

        for key in data:
            if "fd" not in key:
                continue

            _, detail_id, tag = key.split("-")

            # detail_id를 중복없이 리스트에 저장한다.
            if detail_id not in detail_of_diet_ids:
                detail_of_diet_ids.append(detail_id)

            # 디테일 아이디를 키로 하는 딕셔너리에 디테일 정보들을 넣는다.
            if detail_of_diet.get(detail_id) is None:
                # detail_id를 키로 하는 딕셔너리가 없으면 생성
                detail_of_diet[detail_id] = {}
                detail_of_diet[detail_id][tag] = data[key]
            else:
                detail_of_diet[detail_id][tag] = data[key]

        for detail_id in detail_of_diet_ids:
            orm_detail_of_diet = DetailOfDiet()
            # 이미지 저장
            food_image_file_name = (
                str(request.user.id) + detail_id + str(string_save_datetime) + ".jpeg"
            )
            food_image_file_path = os.path.join(
                "static", "media", "user_food_detail", food_image_file_name
            )
            save_image(detail_of_diet[detail_id]["img"], food_image_file_path)

            orm_detail_of_diet.name = detail_of_diet[detail_id]["name"]  # 음식 이름
            orm_detail_of_diet.carbohydrate = detail_of_diet[detail_id][
                "carbohydrate"
            ]  # 탄수화물양
            orm_detail_of_diet.protein = detail_of_diet[detail_id][
                "protein"
            ]  # 단백질양

            orm_detail_of_diet.fat = detail_of_diet[detail_id]["fat"]  # 지방양
            orm_detail_of_diet.calorie = detail_of_diet[detail_id]["calorie"]  # 칼로리
            orm_detail_of_diet.quantity = detail_of_diet[detail_id]["quantity"]  # 양
            orm_detail_of_diet.created_at = save_datetime  # 생성 시간
            orm_detail_of_diet.updated_at = save_datetime  # 수정 시간
            orm_detail_of_diet.diet_id = diet.id  # 식단 아이디
            orm_detail_of_diet.image_path = food_image_file_path  # 음식 이미지 경로
            orm_detail_of_diet.save()

        # 홈으로 redirect
        return HttpResponseRedirect(
            reverse(
                "diet:record_list",
            )
        )

    now, date, time, meal_type = record_date_mealtype()

    # # 직접 입력하는거 구현하기
    return render(
        request,
        "diet/record_add.html",
        {"record_date": date, "record_time": time, "meal_type": meal_type, "now": now},
    )


def record_add_with_recommend(request, food_id):
    # 추천으로 넣는거 구현
    food = get_object_or_404(Food, id=food_id)

    now, date, time, meal_type = record_date_mealtype()

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
            "now": now,
        },
    )


# record_add 페이지를 공유해서 쓰되 전달하는 인자에 차이를 둔다.
def record_edit(request, record_id):
    if request.method == "POST":
        data = request.POST
        save_datetime = timezone.make_aware(
            datetime.now(), timezone.get_default_timezone()
        )
        string_save_datetime = save_datetime.strftime("%Y%m%d%H%M%S")
        image_file_name = str(request.user.id) + str(string_save_datetime) + ".jpeg"
        diet_image_file_path = os.path.join(
            "static", "media", "user_food", image_file_name
        )

        diet = UserDiet.objects.filter(id=record_id).first()

        datetime_list = data["take_at"].strip().split()

        # test
        date_list = [int(i[:-1]) for i in datetime_list[:3]]

        # diet.take_at = convert_string_to_datetime(data["take_at"])
        # diet.take_date = datetime(*date_list).date()
        diet.meal = data["meal"]  # 1: 아침, 2: 점심, 3: 저녁, 4:간식, 5: 야식
        diet.memo = data["meal_memo"]  # 식사 메모
        diet.updated_at = save_datetime  # 수정 시간
        diet.save()

        return HttpResponseRedirect(
            reverse(
                "diet:record_list",
            )
        )

    return render(request, "diet/record_add.html", {"record_id": record_id})


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
        "nickname": UserProfile.objects.get(user_id=request.user).nickname,
        "email": User.objects.filter(id=request.user.id).first().email,
    }

    return render(request, "diet/mypage.html", context)
