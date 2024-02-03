from django.db import models
from django.contrib.auth.models import User


class UserDiet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=100, null=True, blank=True, db_comment="식단 이미지 경로, 사용자가 직접 추가한 식단이면 null")
    take_at = models.DateField(db_comment="식단을 섭취한 날짜")
    meal = models.IntegerField(default=1, db_comment="1은 아침, 2는 점심, 3은 저녁, 4는 간식, 5는 야식")
    memo = models.TextField(null=True, blank=True, db_comment="식단에 대한 메모")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)


class DetailOfDiet(models.Model):
    diet = models.ForeignKey(UserDiet, on_delete=models.CASCADE)
    image_x = models.IntegerField(null=True, blank=True, db_comment="이미지의 x좌표,  사용자가 직접 추가한 식단이면 null")
    image_y = models.IntegerField(null=True, blank=True, db_comment="이미지의 y좌표,  사용자가 직접 추가한 식단이면 null")
    name = models.CharField(max_length=100, db_comment="음식 이름")
    carbohydrate = models.IntegerField(db_comment="100g당 탄수화물")
    protein = models.IntegerField(db_comment="100g당 단백질")
    fat = models.IntegerField(db_comment="100g당 지방")
    calorie = models.IntegerField(db_comment="100g당 칼로리")
    quantity = models.IntegerField(db_comment="몇 인분인지, 1: 소, 2: 중, 3: 대")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Food(models.Model):
    name = models.CharField(max_length=50, db_comment="음식 이름")
    description = models.CharField(max_length=200, db_comment="음식에 대한 설명")
    image_path = models.CharField(max_length=100, db_comment="음식 이미지 경로")
    calorie = models.IntegerField(db_comment="100g당 칼로리")
    carbohydrate = models.IntegerField(db_comment="100g당 탄수화물")
    protein = models.IntegerField(db_comment="100g당 단백질")
    fat = models.IntegerField(db_comment="100g당 지방")
    is_main = models.BooleanField(default=False, db_comment="메인 음식 여부")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
