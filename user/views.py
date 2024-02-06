import json

from django.shortcuts import render, redirect
from django.views import View


# Create your views here.
def index(request):
    return render(request, "user/FLW_SP_001.html")


def login(request):
    return render(request, "user/FLW_OB_001.html")


def agreement(request):
    # 기존 가입자라면 홈으로 redirect

    # 신규 가입자라면 동의 페이지 렌더
    # 세션으로 동의 유지
    context = {
        "age_confirmation": False,
        "terms_of_service_agreement": False,
        "privacy_policy_agreement": False,
        "marketing_consent_agreement": False,
    }

    request.session["user_input"] = context
    # return redirect('appMain:index')

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


# prompt = ""
# if request.method == "POST":
#     # prompt = request.POST['prompt']
#     prompt = request.POST.get("prompt", None)

# get_prediction = request.session.get('prediction', None)
# context = {
# 	'prompt': "",
# 	'result_image': None,
# 	'has_result': False,
# }
# if get_prediction is not None:
# 	context['prompt'] = get_prediction['prompt']
# 	context['result_image'] = get_prediction['result_image']
# 	context['has_result'] = get_prediction['has_result']
# 	del request.session['prediction']
