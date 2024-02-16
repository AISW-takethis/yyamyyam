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
    # TODO 모든 웹페이지에서 로그인되어있지 않은 상태라면 스플래시 화면으로 리다이텍트

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


def age(request):
    return render(request, "user/agreements/popup.html")


def tos(request):
    return render(request, "user/agreements/popup.html")


def pp(request):
    return render(request, "user/agreements/popup.html")


def mc(request):
    return render(request, "user/agreements/popup.html")


def welcome(request):
    user_context = request.session.get("user_input", None)

    agrees = request.POST.getlist("agree[]", False)

    if user_context is not None:
        user_context["age_confirmation"] = "agree_age" in agrees
        user_context["terms_of_service_agreement"] = "agree_tos" in agrees
        user_context["privacy_policy_agreement"] = "agree_pp" in agrees
        user_context["marketing_consent_agreement"] = "agree_mc" in agrees

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
            1 if context["kakao_account"]["gender"] == "male" else 2
        )
    except:
        user_context["gender"] = 1

    try:
        user_context["birth"] = (
            context["kakao_account"]["birthyear"] + context["kakao_account"]["birthday"]
        )
    except:
        user_context["birth"] = None

    request.session["user_input"] = user_context
    return render(request, "user/FLW_INFO_001.html")


def nickname(request):
    context = {"nickname": request.session["user_input"]["nickname"]}
    return render(request, "user/FLW_INFO_002.html", context)


def birth(request):
    user_context = request.session.get("user_input", None)
    nickname = request.POST.get("nickname_input", None)

    if user_context is not None:
        user_context["nickname"] = nickname

    birthday = request.session["user_input"]["birth"]
    birth_year = int(birthday[0:4])
    birth_month = int(birthday[4:6])
    birth_day = int(birthday[6:])

    context = {
        "gender": request.session["user_input"]["gender"],
        "birth_year": birth_year,
        "birth_month": birth_month,
        "birth_day": birth_day,
    }

    request.session["user_input"] = user_context
    return render(request, "user/FLW_INFO_003.html", context)


def physical(request):
    user_context = request.session.get("user_input", None)
    gender = request.POST.get("gender", None)
    year = request.POST.get("year_input", None)
    month = request.POST.get("month_input", None)
    day = request.POST.get("day_input", None)

    if user_context is not None:
        user_context["gender"] = gender
        user_context["birth"] = str(year) + str(month) + str(day)

    request.session["user_input"] = user_context
    return render(request, "user/FLW_INFO_004.html")


def activity(request):
    user_context = request.session.get("user_input", None)
    height = request.POST.get("height_input", None)
    weight = request.POST.get("weight_input", None)

    if user_context is not None:
        user_context["height"] = int(height)
        user_context["weight"] = int(weight)

    request.session["user_input"] = user_context
    return render(request, "user/FLW_INFO_005.html")


def kcal(request):
    user_context = request.session.get("user_input", None)

    if user_context is not None:
        user_context["activity"] = request.POST.get("activity", None)

    request.session["user_input"] = user_context
    return render(request, "user/FLW_INFO_006.html")


def complete(request):
    # user_profile.user_id = request.user.id
    # user_profile.agree_age_confirmation = "agree_age" in agrees
    # user_profile.agree_terms_of_service = "agree_tos" in agrees
    # user_profile.agree_privacy_policy = "agree_pp" in agrees
    # user_profile.agree_marketing_consent = "agree_mc" in agrees
    return redirect("diet:recommand_diet")
