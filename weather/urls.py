from django.conf.urls.static import static

from django.urls import path, include

from rest_framework_swagger.views import get_swagger_view

from weather import settings

api_urls = [path('apis/', include('apps.apis.urls', namespace='apis')), ]
urlpatterns = [
                  path('weather/', include('apps.weather_ui.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

schema_view = get_swagger_view(patterns=api_urls, title='apis')

urlpatterns = urlpatterns + api_urls + [path('docs/', schema_view), ]
