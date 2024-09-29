from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('transactions/api/v1/', include('transactions.urls'), name='transactions'),
    path('users/api/v1/', include('users.urls'), name='users'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

