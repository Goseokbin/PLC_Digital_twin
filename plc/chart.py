import pymysql

conn = pymysql.connect(host='localhost', user='root',password='1234',db='Graduation',charset='utf8')

curs=conn.cursor()

sql = "select *from plc_arduino"
curs.execute(sql)

rows = curs.fetchall()
print(rows)
conn.close()