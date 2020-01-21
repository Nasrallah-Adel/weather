
from django.conf.urls.static import static

from django.urls import path, include

from rest_framework_swagger.views import get_swagger_view

from weather import settings

schema_view = get_swagger_view(title='apis')
urlpatterns = [
                  # path('admin/', admin.site.urls),
                  path('apis/', include('apis.urls', namespace='api')),
                  path('swagger/', schema_view,name='schema_view'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
