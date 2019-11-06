from django.shortcuts import render
import serial
import datetime
from serial import SerialException
from .models import Arduino
from .models import Outlier_data
from .models import Set_Outlier
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pymysql
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as opy
import json
import time
import codecs


# Create your views here.


def index(request):
    return render(request, 'plc/index.html', {});
def table(request):
    return render(request, 'plc/table.html', {});


def history(request):
    return render(request, 'plc/history.html', {});


def base(request):
    return render(request, 'plc/base.html', {});


def dht(request):
    return render(request, 'plc/dht.html', {});


def unity(request):
    return render(request, "plc/webgl.html")


class IndexView(TemplateView):
    template_name = "plc/index.html"


def arduino(request):
    value = Set_Outlier.objects.get(pk=1)
    print(value.h_max)

    try:
        ser = serial.Serial(
             port='/dev/cu.usbserial-A107P4O8',
            #port='COM6',
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

            if float(humi) > value.h_max or float(humi) < value.h_min:
                Outlier_data(value=float(humi), sensor="Humidity").save()
            elif float(temp) > value.t_max or float(temp) < value.t_min:
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


@csrf_exempt
def GetDate(request):
    startdate = request.POST['startdate']
    startdate = startdate.replace('/', '-')
    stdate = startdate[0:12]
    eddate = startdate[21:33]

    conn = pymysql.connect(host='localhost', user='root', password='1234', db='Graduation', charset='utf8')
    sql = "SELECT DATE_FORMAT(date,'%Y-%m-%d %H') m  ,Round(avg(temperature)) as temperature,Round(avg(humidity)) as humidity FROM plc_arduino where date between" + "'" + stdate + "'" + "and" + "'" + eddate + "'" + "GROUP BY m"
    df = pd.read_sql(sql, conn)

    fig = go.Figure()
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
    list_v, list_s, list_t = GetOutlier()
    context = {'MAX_Temperature': MAX_Temperature,
               'MAX_Humidity': MAX_Humidity,
               'sensor': list_s,
               'value': list_v,
               'date': list_t}

    return render(request, 'plc/dht.html', context)


def GetOutlier():
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='Graduation', charset='utf8')
    # sql = "select * from plc_outlier_data order by date desc limit 5"
    sql = "SELECT value,sensor,DATE_FORMAT(date, '%Y/%m/%d %H:%i')as date FROM plc_outlier_data limit 5"
    df = pd.read_sql(sql, conn)
    list_v = list(df.value.values)
    list_s = list(df.sensor.values)
    list_t = list(df.date.values)

    return list_v, list_s, list_t


def OutlierHistory(request):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='Graduation', charset='utf8')
    sql = "SELECT value,sensor,DATE_FORMAT(date, '%Y/%m/%d %H:%i')as date FROM plc_outlier_data "
    sql2 = "SELECT number,DATE_FORMAT(date, '%Y/%m/%d %H:%i')as date FROM plc_outlier order by date desc "

    df = pd.read_sql(sql, conn)
    df2 = pd.read_sql(sql2,conn)
    print(df2)
    date, values, sensor ,date2,number= [], [], [],[],[]
    date = list(df.date.values)
    values = list(df.value.values)
    sensor = list(df.sensor.values)
    date2 = list(df2.date.values)
    number = list(df2.number.values)
    print(date)
    x = date
    y = values
    layout  = go.Layout(
        font=dict(
            size=10,
            color="#00ad5f"
        ),
        paper_bgcolor='rgba(34,34,34,1)',
        plot_bgcolor='rgba(34,34,34,1)',

    )

    data = go.Scatter(x=x, y=y,marker=dict(size=20),
                             mode='markers', opacity=0.8, marker_color='green', text=sensor)
    fig = go.Figure(data=data, layout=layout)

    plot = opy.plot(fig,output_type='div')

    return render(request, "plc/history.html", context={'plot_div': plot,
                                                        'number':number,
                                                        'date':date2})


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
    sql = "update plc_set_outlier set h_max=" + h_max + ",h_min=" + h_min + ",t_max=" + t_max + ",t_min=" + t_min + ",e_max=" + e_max + ",e_min=" + e_min + ",i_max=" + i_max + ",i_min=" + i_min + " where id=1"
    print(sql)
    curs = conn.cursor()
    curs.execute(sql)
    conn.commit()
    conn.close()
    return HttpResponse("이상점 설정이 완료되었습니다")


def getPLC(request):
    ser = serial.Serial(
        port='COM3',
        baudrate=9600,
        timeout=1,
        bytesize=serial.EIGHTBITS,)

    enq=u"\u0005"
    etx = u"\u0004"

    start1 = enq + "00RSS0205%MX2004%MX1" + etx

    out = ''

    # s = codecs.encode(s.encode(), 'hex_codec')
    # get keyboard input
    # ser.write(bytes((chr(37)+s+chr(35)).encode("hex")))

    # ser.write(s.encode("ASCII"))

    # ser.write(bytearray(start1, 'ascii'))
    ser.write(bytearray(start1, 'ascii'))

    # while True:
    #     ser.write(bytearray(start1, 'ascii'))
    #
    #     out = ser.readline()
    #
    #     ser.close()
    #     if out != '':
    #         print(out)
    #     else:
    #         print("out이 없음")
    return render(request,'plc/model.html',context={'id':1})

def setPLC(request):
    ser = serial.Serial(
        port='COM3',
        baudrate=9600,
        timeout=1,
        bytesize=serial.EIGHTBITS, )

    enq = u"\u0005"
    etx = u"\u0004"

    start1 = enq + "00RSS0205%MX2004%MX1" + etx

    out = ''

    # s = codecs.encode(s.encode(), 'hex_codec')
    # get keyboard input
    # ser.write(bytes((chr(37)+s+chr(35)).encode("hex")))

    # ser.write(s.encode("ASCII"))

    # ser.write(bytearray(start1, 'ascii'))
    ser.write(bytearray(start1, 'ascii'))

    while True:
        ser.write(bytearray(start1, 'ascii'))

        out = ser.readline()

        ser.close()
        if out != '':
            print(out)
        else:
            print("out이 없음")
    return render(request, 'plc/model.html', context={'id': 1})

def sendplcoutlier(request):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='Graduation', charset='utf8')
    sql2 = "SELECT number,DATE_FORMAT(date, '%Y/%m/%d %H:%i')as date FROM plc_outlier order by date desc "

    df = pd.read_sql(sql2, conn)
    value = list(df.number.values)
    date = list(df.date.values)
    context={'number':value,
             'date':date}
    print(context)

    return JsonResponse(context, safe=False)


