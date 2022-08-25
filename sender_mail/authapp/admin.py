from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from authapp.forms import CustomUserCreationForm, CustomUserChangeForm
from authapp.models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'age', 'is_staff', 'is_active', 'is_verify', 'date_joined')
    list_filter = ('is_active', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'age', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_verify', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'age', 'password1', 'password2', 'is_active', 'is_staff', 'is_verify'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
