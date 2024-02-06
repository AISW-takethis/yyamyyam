import json

from django.shortcuts import render, redirect
from django.views import View


# Create your views here.
def index(request):
    return render(request, "user/FLW_SP_001.html")


def login(request):
    return render(request, "user/FLW_OB_001.html")
