import pymysql
import requests
import datetime
import pandas as pd
import plotly.graph_objects as go

def GetOutlier() :
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='Graduation', charset='utf8')
    sql = "SELECT MAX(temperature) from plc_arduino"
    sql2 = "SELECT MAX(humidity) from plc_arduino"
    curs = conn.cursor()
    curs.excute(sql)

    rows = curs.fetchall()
    print(rows)
    # df = pd.read_sql(sql, conn)
    # df2 = pd.read_sql(sql2, conn)
    # print(df)
    # print(df2)
