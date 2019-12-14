from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.contrib.auth import get_user_model
from .forms import SignupForm, MyPasswordChangeForm

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
