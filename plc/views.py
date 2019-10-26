from django.shortcuts import render
import serial
import datetime
import json
from serial import SerialException
from django.core import serializers
from .models import Arduino
from .models import Outlier_data
from django.views.generic import View
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pymysql
import pandas as pd
import plotly.graph_objects as go


# Create your views here.


def index(request):
    return render(request, 'plc/index.html', {});


def model(request):
    return render(request, 'plc/model.html', {});


def history(request):
    return render(request, 'plc/history.html', {});


def header(request):
    return render(request, 'plc/header.html', {});


def real(request):
    return render(request, 'plc/real.html', {});


def dht(request):
    return render(request, 'plc/dht.html', {});


def chart(request):
    return render(request, 'plc/chart.html', {});


class IndexView(TemplateView):
    template_name = "plc/index.html"


def arduino(request):
    try:
        ser = serial.Serial(
            # port='/dev/cu.usbserial-A107P4O8',
            port='COM6',
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

            if float(humi) > 50:
                Outlier_data(value=float(humi), sensor="Humidity").save()
            elif float(temp) > 25:
                Outlier_data(value=float(humi), sensor="Temperature").save()
            else:
                Arduino(temperature=float(temp), humidity=float(humi)).save()
            context = {'temperature': float(temp),
                       'humi': float(humi),
                       'date': date,
                       'time': time}
        return JsonResponse(context, safe=False)



    except SerialException:
        print("No HttpResponseconnect")
        return HttpResponse("No HttpResponseconnect")


def GetArduino(request):
    ardu = Arduino.objects.all().values("temperature", "humidity", "date")
    # print(ardu)
    ardu_list = list(ardu)
    print(ardu_list)
    return JsonResponse(ardu_list, safe=False)


def GetArduino2(request):
    data = arduino(request)
    print(data)
    return JsonResponse(data, safe=False)


def unity(request):
    return render(request, "plc/webgl.html")


@csrf_exempt
def GetDate(request):
    startdate = request.POST['startdate']
    startdate = startdate.replace('/', '-')
    stdate = startdate[0:12]
    eddate = startdate[21:33]

    conn = pymysql.connect(host='localhost', user='root', password='1234', db='Graduation', charset='utf8')
    sql = "SELECT DATE_FORMAT(date,'%Y-%m-%d %H') m  ,Round(avg(temperature)) as temperature,Round(avg(humidity)) as humidity FROM plc_arduino where date between"+ "'"+stdate+"'"+ "and"+ "'"+eddate+"'" +"GROUP BY m"
    df = pd.read_sql(sql, conn)

    fig = go.Figure()
    print(df)
    fig.add_trace(go.Scatter(
        x=df.m,
        y=df['temperature'],
        name="Temperature",
        line_color='deepskyblue',
        opacity=0.8))

    fig.add_trace(go.Scatter(
        x=df.m,
        y=df['humidity'],
        name="humidity",
        line_color='dimgray',
        opacity=0.8))

    fig.show()
    conn.close()
    return JsonResponse(startdate, safe=False)


def GetMaxdata(request):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='Graduation', charset='utf8')
    sql = "SELECT MAX(temperature) from plc_arduino"
    sql2 = "SELECT MAX(humidity) from plc_arduino"
    df = pd.read_sql(sql, conn)
    df2 = pd.read_sql(sql2, conn)
    MAX_Temperature = int(df.values[0])
    MAX_Humidity = int(df2.values[0])
    list_v,list_s,list_t=GetOutlier()
    context = {'MAX_Temperature': MAX_Temperature,
               'MAX_Humidity': MAX_Humidity,
               'sensor':list_s,
               'value':list_v,
               'date':list_t}

    return render(request, 'plc/dht.html', context)


def GetOutlier():
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='Graduation', charset='utf8')
    # sql = "select * from plc_outlier_data order by date desc limit 3"
    sql ="SELECT value,sensor,DATE_FORMAT(date, '%Y/%m/%d %H:%i')as date FROM plc_outlier_data limit 3"
    df = pd.read_sql(sql, conn)
    list_v =list(df.value.values)
    list_s = list(df.sensor.values)
    list_t = list(df.date.values)

    return list_v,list_s,list_t

@csrf_exempt
def SetOutlier(request):
    t_max = request.POST["t_max"]
    t_min = request.POST["t_min"]
    h_max = request.POST["h_max"]
    h_min = request.POST["h_min"]
    e_max = request.POST["e_max"]
    e_min = request.POST["e_min"]
    i_max = request.POST["i_max"]
    i_min = request.POST["i_max"]

    conn = pymysql.connect(host='localhost', user='root', password='1234', db='Graduation', charset='utf8')
    sql = "update plc_set_outlier set h_max="+h_max+",h_min="+h_min+",t_max="+t_max+",t_min="+t_min+",e_max="+e_max+",e_min="+e_min+",i_max="+i_max+",i_min="+i_min+" where id=1"
    print(sql)
    curs = conn.cursor()
    curs.execute(sql)
    conn.commit()
    conn.close()
    return render(request,'plc/history.html')
