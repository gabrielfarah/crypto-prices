from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from coins import settings

urlpatterns = [
    # URLS pre-built used by rest_auth, these must be changes for a better template
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns += [path('', include('website.urls')), path('i18n/', include('django.conf.urls.i18n'))]
