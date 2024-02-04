from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'user/FLW_SP_001.html')