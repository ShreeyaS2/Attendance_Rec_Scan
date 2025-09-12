from django.shortcuts import render, redirect
from polls.models import Sign, Log
from .forms import SignForm, LogForm
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import logout
import requests
from django.http import HttpResponse
import json
from django.template import loader
from .face_recognition_utils import recognize_faces_django, train_model_from_django

# Create your views here.

def conf(request):
    return render(request, "confirmation.html")

def polls(request):
    if request.method == "POST":
        form = SignForm(request.POST)
        name = request.POST["name"]
        perm_id=request.POST["perm_id"]
        password = request.POST["password"]
        image=request.FILES.get('image')
        data = Sign(name = name, perm_id=perm_id, password = password, image=image)
        data.save()
        return HttpResponseRedirect('face_recognition_result.html')
    
    else:
        form = SignForm()


    return render(request, "polls.html", {'form':form})

def face_recognition_result(request):
    """New view to handle face recognition and display results"""
    recognized_students = recognize_faces_django()
    
    context = {
        'recognized_students': recognized_students,
        'total_students': Sign.objects.count(),
    }
    
    return render(request, "face_recognition_result.html", context)

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

