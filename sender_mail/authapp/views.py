from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.shortcuts import get_object_or_404

from authapp.forms import CustomAuthenticationForm, CustomUserCreationForm
from authapp.models import VerifyCode
from authapp.services import is_token_verify_expired
from authapp.tasks import send_verify_email


# class AuthorizationUserView():


class MainPageView(TemplateView):
    template_name = 'index.html'


class UserLoginView(LoginView):
    form_class = CustomAuthenticationForm
    success_url = '/'


class UserLogoutView(LogoutView):
    template_name = 'index.html'


class RegistrationUserView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/regist.html'
    success_url = reverse_lazy('notificatio_after_registrtion')

    def form_valid(self, form):
        res = super().form_valid(form)
        user = self.object
        verify_code = VerifyCode.objects.create(user=user)
        send_verify_email.delay(user.email, verify_code.token)
        return res


class NotificationAfterRegistrationView(TemplateView):
    template_name = 'registration/notification_verify_by_mail.html'


class VerifyView(TemplateView):
    template_name = 'registration/verification.html'

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        verify_obj = get_object_or_404(VerifyCode, token=token)
        user = verify_obj.user
        if is_token_verify_expired(verify_obj):
            user.is_verify = True
            user.is_active = True
            with transaction.atomic():
                user.save(update_fields=['is_active', 'is_verify'])
                verify_obj.delete()
        else:
            verify_obj.delete()
        context = self.get_context_data(**kwargs)
        context.update({'user': user})
        return self.render_to_response(context)


@login_required
def call_exception_view(request):
    raise ValueError('Test error')
