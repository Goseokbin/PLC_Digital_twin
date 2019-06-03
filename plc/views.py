from django.shortcuts import render
import serial
import datetime
import json
from serial import SerialException
from django.core import serializers
from .models import Arduino
from django.views.generic import View
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, 'plc/index.html',{});

def model(request):
    return render(request, 'plc/model.html',{});

def history(request):
    return render(request, 'plc/history.html',{});

def real(request):
    return render(request, 'plc/real.html',{});

def dht(request):
    return render(request, 'plc/dht.html',{});

def barchart(request):
    return render(request, 'plc/barchart.html',{});

class IndexView(TemplateView):
    template_name = "plc/index.html"

def arduino(request):

    try:
        ser = serial.Serial(
            port='/dev/cu.usbserial-A107P4O8',
            baudrate=9600,
        )


        if ser.readable():
             res = ser.readline()
             decoderes = res.decode()[:len(res) - 1]
             print(decoderes)
             humi = decoderes[5:9]
             temp = decoderes[0:4]
             dt = datetime.datetime.now()
             date = dt.strftime('%Y-%m-%d')
             time = dt.strftime('%H:%M:%S')
            # # Arduino(temperature=float(temp),humidity=float(humi)).save()
             context = {'temperature': float(temp),
               'humi': float(humi),
               'date': date,
               'time': time}
        return JsonResponse(context, safe=False)



    except SerialException:
        print("No HttpResponseconnect")
        return HttpResponse("No HttpResponseconnect")


def GetArduino(request):
    ardu= Arduino.objects.all().values("temperature","humidity","date")
    #print(ardu)
    ardu_list=list(ardu)
    print(ardu_list)
    return JsonResponse(ardu_list,safe=False)

def GetArduino2(request):
    data=arduino(request)
    print(data)
    return JsonResponse(data,safe=False)
