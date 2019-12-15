from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def index(request):
	user = User.objects.filter(id=request.user.id).first()
	try:
		if (user.profile_picture, None):
			image_url = user.profile_picture.url
		return render(request,'homepage/index.html', {'image_url': image_url})
	except:
		return render(request, 'homepage/index.html', {'image_url': None})


def home(request):
	return render(request,'homepage/home.html')