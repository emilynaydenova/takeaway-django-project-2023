from decouple import config
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Takeaway import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('app.urls')),
    path('accounts/', include('accounts.urls')),
]

if config('USE_S3') == 'False':  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

