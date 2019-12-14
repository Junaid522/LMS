from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
	return render(request,'homepage/index.html')


def home(request):
	return render(request,'homepage/home.html')