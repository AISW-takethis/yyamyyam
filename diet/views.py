from django.shortcuts import render


# Create your views here.
def recommand(request):
    return render(request, "diet/recommand.html", {})


def record_list(request):
    return render(request, "diet/record_list.html", {})


def record_add(request):
    return render(request, "diet/record_add.html", {})
