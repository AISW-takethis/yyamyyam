from django.shortcuts import render


# Create your views here.
def recommand(request):
    return render(request, "diet/recommand.html", {})


def diet(request):
    pass
