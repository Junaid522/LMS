from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'created_at', 'is_active','first_name', 'last_name', 'email',)
    list_display_links = ('first_name', 'last_name', 'email',)
    search_fields = ('id', 'first_name', 'email')
    ordering = ['-id', ]


admin.site.register(User, UserAdmin)
