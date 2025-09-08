from django.contrib import admin
from django.urls import path

from . import views
# from .views import polls, thankYou

urlpatterns = [
    #path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('', views.polls),
    path('confirmation.html', views.conf),
]