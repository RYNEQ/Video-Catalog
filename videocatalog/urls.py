from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('django.contrib.auth.urls')),
    path('api/', include('rest_framework.urls')),
    path('api/', include('core.apiurls', namespace='coreapi')),
    # path('api/', include('payment')),
    # path('api/', include('user')),
    path('', include('core.urls', namespace='core')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
