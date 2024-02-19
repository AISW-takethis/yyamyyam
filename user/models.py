from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agree_age_confirmation = models.BooleanField(default=False)
    agree_terms_of_service = models.BooleanField(default=False)
    agree_privacy_policy = models.BooleanField(default=False)
    agree_marketing_consent = models.BooleanField(default=False)
    nickname = models.CharField(max_length=20, null=True)
    gender = models.IntegerField(default=1, db_comment="1은 남성, 2는 여성")
    birth = models.DateField(null=True)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    level_of_activity = models.IntegerField(
        default=1,
        db_comment="1은 앉아서 일하는 경우, 2는 가벼운 활동을 하는 경우, 3은 보통 활동을 하는 경우, 4는 매우 활동적인 경우",
    )
    recommend_daily_calorie = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
