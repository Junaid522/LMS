import os

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.contrib.auth import get_user_model

# from Library_Management_System.Library_Management_System.settings import MEDIA_ROOT
from .forms import SignupForm, MyPasswordChangeForm

from django.views.decorators.csrf import csrf_exempt


User = get_user_model()


class SignUp(generic.CreateView):
    form_class = SignupForm
    model = User
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class PasswordResetView(LoginRequiredMixin, View):
    form_class = MyPasswordChangeForm
    template_name = 'profile_change_password.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        form = self.form_class(self.request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)

        if form.is_valid():
            form.save()
        return render(request, self.template_name, {'form': form})


class UserPasswordResetView(PasswordResetView, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser

    def get_user(self, user_id):
        return User.objects.filter(id=user_id).first()

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        form = self.form_class(self.get_user(user_id))
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        form = self.form_class(self.get_user(user_id), request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('users_list'))
        return render(request, self.template_name, {'form': form})


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


def getpage(request):
    template_name = 'webcam.html'
    return render(request, template_name=template_name)


@csrf_exempt
def saveimage(request):
    if request.method == 'POST':
        # save it somewhere
        user = User.objects.filter(id=request.user.id).first()
        f = open(MEDIA_ROOT + '/profile-pictures/someimage.jpg', 'wb')
        f.write(request.body)
        print(request.body)
        f.close()
        user.profile_picture = '/profile-pictures/someimage.jpg'
        user.save()
        # return the URL
        return HttpResponse('http://localhost:8000/media/profile-pictures/someimage.jpg')
    else:
        return HttpResponse('no data')


# class CaptureImageView(View):
#     template_name = 'webcam.html'

    # def get(self, request, *args, **kwargs):
    #     return render(request, template_name=self.template_name)
    #
    # # @method_decorator(csrf_exempt)
    # def post(self, request, *args, **kwargs):
    #     if request.POST:
    #         # save it somewhere
    #         f = open(MEDIA_ROOT + '/webcamimages/someimage.jpg', 'wb')
    #         f.write(request.raw_post_data)
    #         f.close()
    #         # return the URL
    #         return HttpResponse('http://localhost:8000/media/webcamimages/someimage.jpg')
    #     else:
    #         return HttpResponse('no data')