from django.shortcuts import render


# Create your views here.
def recommend(request):
    return render(request, "diet/recommend.html", {})


def record_list(request):
    return render(request, "diet/record_list.html", {})


def record_add(request):
    return render(request, "diet/record_add.html", {})


def record_detail(request):
    return render(request, "diet/record_detail.html", {})


# record_add 페이지를 공유해서 쓰되 전달하는 인자에 차이를 둔다.
def record_edit(request):
    return render(request, "diet/record_add.html", {})


def record_detail_search(request):
    item_list = [i for i in range(1, 11)]
    return render(request, "diet/record_detail_search.html", {"item_list": item_list})


def loading(request):
    return render(request, "loading.html", {})
