from django.contrib import admin
from django.urls import path, include
from allauth.account.views import ConfirmEmailView
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('randomizer.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
]   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
