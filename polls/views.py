from django.shortcuts import render, redirect
from polls.models import Sign, Log
from .forms import SignForm, LogForm
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
import requests
from django.http import HttpResponse
import json
from django.template import loader

# Create your views here.

def thanks(request):
    return render(request, "index.html")

def stat(request):
    return render(request, "statistics.html")
    
def thanks1(request):
    return render(request, "index1.html")

def thankYou(request):
    return render(request, "index copy.html")

def committee(request):
    return render(request, "committees.html")

def sec(request):
    return render(request, "secretariat.html")

def ver(request):
    return render(request, "veritas.html")

def feat(request):
    return render(request, "features.html")

def team(request):
    return render(request, "team.html")

def brand(request):
    return render(request, "branding.html")

def feat1(request):
    return render(request, "features copy.html")

def team1(request):
    return render(request, "team copy.html")

def committee1(request):
    return render(request, "committees1.html")

def sec1(request):
    return render(request, "secretariat1.html")

def ver1(request):
    return render(request, "veritas1.html")

def doc(request):
    return render(request, "documents.html")

def brochure(request):
    return render(request, "brochure.html")

def form(request):
    return render(request, "form.html")

def polls(request):
    if request.method == "POST":
        form = SignForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        data = Sign(username = username, password = password)
        data.save()
        return HttpResponseRedirect('form.html')
    
    else:
        form = SignForm()


    return render(request, "polls.html", {'form':form})

def polls1(request):
    if request.method == "POST":
        form = LogForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        data = Log(username = username, password = password)
        data.save()
        return HttpResponseRedirect('index.html')
    
    else:
        form = LogForm()


    return render(request, "polls copy.html", {'form':form})

def logout_view(request):
    logout(request)
    return redirect(request, "index.html")

