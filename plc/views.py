from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


def index(request):
    return render(request, 'plc/index.html',{});

def model(request):
    return render(request, 'plc/model.html',{});

def history(request):
    return render(request, 'plc/history.html',{});

def real(request):
    return render(request, 'plc/real.html',{});