from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


from authapp.views import MainPageView, UserLoginView, UserLogoutView, NotificationAfterRegistrationView, \
    RegistrationUserView, VerifyView, call_exception_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.as_view(), name='index'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('notification', NotificationAfterRegistrationView.as_view(), name='notificatio_after_registrtion'),
    path('registration', RegistrationUserView.as_view(), name='registration'),
    path('verify/<str:token>', VerifyView.as_view(), name='verify'),
    path('exception/', call_exception_view, name='call_error'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
