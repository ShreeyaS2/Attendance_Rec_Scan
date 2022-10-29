from django.contrib import admin
from django.urls import path

from . import views
# from .views import polls, thankYou

urlpatterns = [
    #path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('polls.html', views.polls),
    path('polls copy.html', views.polls1),
    path('', views.thankYou),
    path('index.html', views.thanks1),
    path('index1.html', views.thanks),
    path('statistics.html', views.stat),
    path('index copy.html', views.thankYou),
    path('committees.html', views.committee),
    path('secretariat.html', views.sec),
    path('veritas.html', views.ver),
    path('features.html', views.feat),
    path('team.html', views.team),
    path('features copy.html', views.feat1),
    path('team copy.html', views.team1),
    path('branding.html', views.brand),
    path('committees1.html', views.committee1),
    path('secretariat1.html', views.sec1),
    path('veritas1.html', views.ver1),
    path('brochure.html', views.brochure),
    path('documents.html', views.doc),
    path('form.html', views.form),
]