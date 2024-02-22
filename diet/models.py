from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class UserDiet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_path = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_comment="식단 이미지 경로, 사용자가 직접 추가한 식단이면 null",
    )
    take_date = models.DateField(db_comment="식단을 섭취한 날짜")

    meal = models.IntegerField(
        default=1, db_comment="1은 아침, 2는 점심, 3은 저녁, 4는 간식, 5는 야식"
    )
    memo = models.TextField(null=True, blank=True, db_comment="식단에 대한 메모")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    take_at = models.DateTimeField(
        db_comment="식단을 섭취한 날짜 및 시간", default=datetime.now()
    )


class DetailOfDiet(models.Model):
    diet = models.ForeignKey(UserDiet, on_delete=models.CASCADE)
    # image_x_start = models.IntegerField(
    #     null=True,
    #     blank=True,
    #     db_comment="이미지의 x 시작좌표,  사용자가 직접 추가한 식단이면 null",
    # )
    # image_x_end = models.IntegerField(
    #     null=True,
    #     blank=True,
    #     db_comment="이미지의 x 끝좌표,  사용자가 직접 추가한 식단이면 null",
    # )
    # image_y_start = models.IntegerField(
    #     null=True,
    #     blank=True,
    #     db_comment="이미지의 y 시작좌표,  사용자가 직접 추가한 식단이면 null",
    # )
    # image_y_end = models.IntegerField(
    #     null=True,
    #     blank=True,
    #     db_comment="이미지의 y 끝좌표,  사용자가 직접 추가한 식단이면 null",
    # )
    image_path = models.CharField(max_length=200, db_comment="음식 이미지 경로")
    name = models.CharField(max_length=100, db_comment="음식 이름")
    carbohydrate = models.FloatField(db_comment="1인분당 탄수화물")
    protein = models.FloatField(db_comment="1인분당 단백질")
    fat = models.FloatField(db_comment="1인분당 지방")
    calorie = models.FloatField(db_comment="1인분당 칼로리")
    quantity = models.FloatField(db_comment="m.n 인분(0.5, 1, 1.5, 2 인분 설정 가능)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Food(models.Model):
    name = models.CharField(max_length=50, db_comment="음식 이름")
    description = models.CharField(max_length=200, db_comment="음식에 대한 설명")
    carbohydrate = models.FloatField(db_comment="1인분당 탄수화물")
    protein = models.FloatField(db_comment="1인분당 단백질")
    fat = models.FloatField(db_comment="1인분당 지방")
    calorie = models.FloatField(db_comment="1인분당 칼로리")
    is_main = models.BooleanField(default=False, db_comment="메인 음식 여부")
