from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    terms_agree = models.BooleanField(default=True)
    agree_of_marketing = models.BooleanField(default=False)
    nickname = models.CharField(max_length=20)
    sex = models.IntegerField(default=1, db_comment="1은 남성, 2는 여성")
    birth = models.DateField()
    height = models.IntegerField()
    weight = models.IntegerField()
    goal_weight = models.IntegerField()
    level_of_activity = models.IntegerField(default=1, db_comment="1은 앉아서 일하는 경우, 2는 가벼운 활동을 하는 경우, 3은 보통 활동을 하는 경우, 4는 매우 활동적인 경우")
    recommend_daily_calorie = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
