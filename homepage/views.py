from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse

from .forms import ImageUploadForm

User = get_user_model()


@login_required
def index(request):
	user = User.objects.filter(id=request.user.id).first()
	form = ImageUploadForm(instance=user)
	try:
		if (user.profile_picture, None):
			image_url = user.profile_picture.url
		return render(request,'homepage/index.html', {'image_url': image_url, 'form': form})
	except:
		return render(request, 'homepage/index.html', {'image_url': None, 'form': form})


@login_required
def upload_image(request):
	user = User.objects.filter(id=request.user.id).first()
	form_class = ImageUploadForm()
	form = form_class(request.FILES, instance=user)
	if form.is_valid():
		form.save()
		return redirect(reverse('index'))


def home(request):
	return render(request,'homepage/home.html')