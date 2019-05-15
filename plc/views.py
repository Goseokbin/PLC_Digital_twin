from django.shortcuts import render
import serial
from serial import SerialException
from .models import Arduino
from django.views.generic import View
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



def arduino(request):
    url = "http://127.0.0.1:8000/"
    try:
        ser = serial.Serial(
            port='/dev/cu.usbserial-A107P4O8',
            baudrate=9600,
        )


        if ser.readable():
             res = ser.readline()
             decoderes = res.decode()[:len(res) - 1]
             print(decoderes)
             temp = decoderes[10:15]
             humi = decoderes[31:36]
             Arduino(temperature=float(temp),humidity=float(humi)).save()


    except SerialException:
        print("No connect")
    return render(request, 'plc/temp.html',{'temp':temp,'humi':humi});

@property
def Arduino_save():
    url = "http://127.0.0.1:8000/"
    try:
        ser = serial.Serial(
            port='/dev/cu.usbserial-A107P4O8',
            baudrate=9600,
        )
        while(ser.readable()):
            if ser.readable():
             res = ser.readline()
             decoderes = res.decode()[:len(res) - 1]
             print(decoderes)
             temp = decoderes[10:15]
             humi = decoderes[31:36]
             print(temp,humi);
             Arduino(temperature=float    (temp), humidity = float(humi)).save()


    except SerialException:
        print("No connect")

class IndexView(TemplateView):
     template_name="plc/index.html"
     #Arduino_save()

def GetArduino(request):
    ardu= Arduino.objects.all()
    context = {'ardu':ardu}

    return render(request,'plc/chart.html',context )


     
