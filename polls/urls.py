from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
# from .views import polls, thankYou

urlpatterns = [
    #path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('', views.polls),
    path('confirmation.html', views.conf),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)