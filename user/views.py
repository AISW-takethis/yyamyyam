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

gender_male = 1
gender_female = 2


# Create your views here.
def splash(request):
	return render(request, "user/FLW_SP_001.html")


def login(request):
	if request.user.is_authenticated:
		return redirect("diet:recommend_diet")
	return render(request, "user/FLW_OB_001.html")


def agreement(request):
	# 기존 가입자라면 홈으로 redirect
	if request.user.is_authenticated:
		if UserProfile.objects.filter(user_id = request.user.id).exists():
			return redirect("diet:recommend_diet")
	else:
		return redirect("user:splash")
	
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
	if not request.user.is_authenticated:
		return redirect("user:splash")
	user_context = request.session.get("user_input", None)
	
	agrees = request.POST.getlist("agree[]", False)
	
	if user_context is not None:
		user_context["age_confirmation"] = "agree_age" in agrees
		user_context["terms_of_service_agreement"] = "agree_tos" in agrees
		user_context["privacy_policy_agreement"] = "agree_pp" in agrees
		user_context["marketing_consent_agreement"] = "agree_mc" in agrees
	
	user_data = json.dumps(list(SocialAccount.objects.filter(user_id = request.user.id).values("extra_data")))
	user_data = user_data[1:-1]
	context = {"user_data": json.loads(user_data)}
	context = context["user_data"]["extra_data"]
	
	try:
		user_context["nickname"] = context["kakao_account"]["profile"]["nickname"]
	except:
		user_context["nickname"] = None
	
	try:
		user_context["gender"] = (
			gender_male
			if context["kakao_account"]["gender"] == "male"
			else gender_female
		)
	except:
		user_context["gender"] = gender_male
	
	try:
		user_context["birth"] = (context["kakao_account"]["birthyear"] + context["kakao_account"]["birthday"])
	except:
		user_context["birth"] = None
	
	request.session["user_input"] = user_context
	return render(request, "user/FLW_INFO_001.html")


def nickname(request):
	if not request.user.is_authenticated:
		return redirect("user:splash")
	context = {"nickname": request.session["user_input"]["nickname"]}
	return render(request, "user/FLW_INFO_002.html", context)


def birth(request):
	if not request.user.is_authenticated:
		return redirect("user:splash")
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
	if not request.user.is_authenticated:
		return redirect("user:splash")
	user_context = request.session.get("user_input", None)
	gender = request.POST.get("gender", None)
	year = request.POST.get("year", None)
	month = request.POST.get("month", None)
	day = request.POST.get("day", None)
	
	if user_context is not None:
		user_context["gender"] = gender
		user_context["birth"] = str(year) + "-" + str(month) + "-" + str(day)
	
	request.session["user_input"] = user_context
	return render(request, "user/FLW_INFO_004.html")


def activity(request):
	if not request.user.is_authenticated:
		return redirect("user:splash")
	user_context = request.session.get("user_input", None)
	height = request.POST.get("height_input", None)
	weight = request.POST.get("weight_input", None)
	
	if user_context is not None:
		user_context["height"] = int(height)
		user_context["weight"] = int(weight)
	
	request.session["user_input"] = user_context
	return render(request, "user/FLW_INFO_005.html")


def kcal(request):
	from datetime import datetime
	
	if not request.user.is_authenticated:
		return redirect("user:splash")
	
	user_context = request.session.get("user_input", None)
	
	gender = request.session["user_input"]["gender"]
	weight = request.session["user_input"]["weight"]
	height = request.session["user_input"]["height"]
	birth_date = request.session["user_input"]["birth"]
	activity = request.POST.get("activity", None)
	
	today = datetime.now()
	birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
	age = (today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day)))
	
	if gender == gender_male:
		bmr = 66.47 + (13.75 * weight) + (5 * height) - (6.76 * age)
	else:
		bmr = 655.1 + (9.56 * weight) + (1.85 * height) - (4.68 * age)
	
	if activity == '1':
		kcal = bmr * 1.2
	elif activity == '2':
		kcal = bmr * 1.375
	elif activity == '3':
		kcal = bmr * 1.555
	else:
		kcal = bmr * 1.725
	
	margin = 200
	percentage = int(((kcal - (bmr * 1.2 - margin)) / ((bmr * 1.725 + margin) - (bmr * 1.2 - margin))) * 100)
	
	kcal = int(kcal)
	context = {
		"nickname": request.session["user_input"]["nickname"],
		"kcal": kcal,
		"percentage": int(percentage),
	}
	
	if user_context is not None:
		user_context["activity"] = activity
		user_context["recommend_kcal"] = kcal
	
	request.session["user_input"] = user_context
	return render(request, "user/FLW_INFO_006.html", context)


def complete(request):
	if not request.user.is_authenticated:
		return redirect("user:splash")
	
	user_profile.user_id = request.user.id
	user_profile.agree_age_confirmation = request.session["user_input"]["age_confirmation"]
	user_profile.agree_terms_of_service = request.session["user_input"]["terms_of_service_agreement"]
	user_profile.agree_privacy_policy = request.session["user_input"]["privacy_policy_agreement"]
	user_profile.agree_marketing_consent = request.session["user_input"]["marketing_consent_agreement"]
	user_profile.nickname = request.session["user_input"]["nickname"]
	user_profile.gender = request.session["user_input"]["gender"]
	user_profile.birth = request.session["user_input"]["birth"]
	user_profile.height = request.session["user_input"]["height"]
	user_profile.weight = request.session["user_input"]["weight"]
	user_profile.activity = request.session["user_input"]["activity"]
	user_profile.recommend_daily_calorie = request.session["user_input"]["recommend_kcal"]
	
	user_profile.save()
	
	return redirect("diet:recommend_diet")
