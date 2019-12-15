from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(verbose_name='First Name', max_length=150)
    last_name = models.CharField(verbose_name='Last Name', max_length=150)
    email = models.EmailField(verbose_name='Email', unique=True, max_length=75)
    username = models.CharField(verbose_name='Username', null=True, max_length=150, default=None, blank=True)
    profile_picture = models.ImageField(upload_to='profile-pictures/', blank=True, max_length=4294967295)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    experience = models.IntegerField(verbose_name='Experience', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return 'Id:{0} Name :{1} {2}, email: {3}'.format(self.id, self.first_name, self.last_name, self.email)