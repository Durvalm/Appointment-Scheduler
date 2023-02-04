from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.scheduler.urls')),
    path('accounts/', include('apps.users.urls')),
    path('backoffice/', include('apps.backoffice.urls')),
    path('employee/', include('apps.barbers.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
