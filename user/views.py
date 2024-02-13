import json

from django.shortcuts import render, redirect
from django.views import View

from django.core import serializers
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from user.models import UserProfile

import json

user = User()
user_profile = UserProfile()
social_account = SocialAccount()


# Create your views here.
def index(request):
    return render(request, "user/FLW_SP_001.html")


def login(request):
    # if request.user.is_authenticated:
    #     return redirect("diet:recommand_diet")
    return render(request, "user/FLW_OB_001.html")


def agreement(request):
    # 기존 가입자라면 홈으로 redirect
    # if request.user.is_authenticated:
    #     # request.user.id
    #     if UserProfile.objects.filter(user_id=request.user.id).exists():
    #         return redirect("diet:recommand_diet")

    # 신규 가입자라면 동의 페이지 렌더
    # 세션으로 동의 유지

    context = {
        "age_confirmation": False,
        "terms_of_service_agreement": False,
        "privacy_policy_agreement": False,
        "marketing_consent_agreement": False,
    }

    request.session["user_input"] = context

    return render(request, "user/FLW_AG_001.html")


# date = request.POST.getlist('agree[]')


def age(request):
    return render(request, "user/agreements/popup.html")


def tos(request):
    return render(request, "user/agreements/popup.html")


def pp(request):
    return render(request, "user/agreements/popup.html")


def mc(request):
    return render(request, "user/agreements/popup.html")


def welcome(request):
    # user_profile.user_id = request.user.id

    agrees = request.POST.getlist("agree[]", False)
    # user_profile.agree_age_confirmation = "agree_age" in agrees
    # user_profile.agree_terms_of_service = "agree_tos" in agrees
    # user_profile.agree_privacy_policy = "agree_pp" in agrees
    # user_profile.agree_marketing_consent = "agree_mc" in agrees

    user_context = {
        "age_confirmation": "agree_age" in agrees,
        "terms_of_service_agreement": "agree_tos" in agrees,
        "privacy_policy_agreement": "agree_pp" in agrees,
        "marketing_consent_agreement": "agree_mc" in agrees,
    }

    user_data = json.dumps(
        list(SocialAccount.objects.filter(user_id=request.user.id).values("extra_data"))
    )
    user_data = user_data[1:-1]
    context = {"user_data": json.loads(user_data)}
    context = context["user_data"]["extra_data"]

    try:
        user_context["nickname"] = context["kakao_account"]["profile"]["nickname"]
    except:
        user_context["nickname"] = None

    try:
        user_context["gender"] = (
            1 if context["kakao_account"]["gender"] == "male" else 0
        )
    except:
        user_context["gender"] = 1

    try:
        user_context["birth"] = (
            context["kakao_account"]["birthyear"] + context["kakao_account"]["birthday"]
        )
    except:
        user_context["birth"] = None

    request.session["prediction"] = user_context
    return render(request, "user/FLW_INFO_001.html")
