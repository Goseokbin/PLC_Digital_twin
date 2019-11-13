from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
import random
import serial
import asyncio
import json


class plcConsumer(AsyncConsumer):
    flag = 0
    ser = 0
    send_flag = 0
    receive_flag = 0

    async def start_periodic_task(self):
        print("connecting")

        enq = u"\u0005"
        etx = u"\u0004"
        # read할 device의 명령어
        op = enq + "00RSS1004%MX104%MX204%MX304%MX404%MX504%MX604%MX704%MX804%MX904%MX005%MX1005%MX1105%MX1205%MX2005%MX2106%IX009" + etx

        # while True:
        #         #     # ser가 열려있을 때에만 실행
        #         #     if (self.ser.isOpen() == False):
        #         #         print("Port is not Open")
        #         #         break
        #         #     else:
        #         #         try:
        #         #             # device 정보 읽어온다.
        #         #             self.ser.write(bytearray(op, 'ascii'))
        #         #             o = self.ser.readline()
        #         #             print(o)
        #         #
        #         #             # 0.15초간 대기
        #         #             await asyncio.sleep(0.05)
        #         #
        #         #             # send_flag가 0일때에만 전송
        #         #             if (self.send_flag == 0):
        #         #                 # receive_flag를 1로 설정하여 send하는 도중에는 receive 못하도록 설정
        #         #                 self.receive_flag = 1
        #         #                 await self.send({
        #         #                     'type': 'websocket.send',
        #         #                     'text': str(o),
        #         #                 })
        #         #                 self.receive_flag = 0
        #         #             else:
        #         #                 print("전송중")
        #         #         except Exception as e:
        #         #             print(e)

    async def websocket_connect(self, event):
        print("connected", event)

        # serial open
    #     self.ser = serial.Serial(
    #         port='COM3',
    #         baudrate=9600,
    #         timeout=0.5,
    #         bytesize=serial.EIGHTBITS,
    #     )
    #
    #     try:
    #         # server accept
    #         await self.send({
    #             "type": "websocket.accept"
    #         })
    #     except Exception as e:
    #         print(e)
    #     # 반복 loop 생성
    #     asyncio.create_task(self.start_periodic_task())
    #
    # async def websocket_receive(self, event):
    #     print("receive", event)
    #     device_len = ''
    #
    #     # sleep(0.05)
    #     # receive_flag가 0일때에만 실행한다.
    #     if (self.receive_flag == 0):
    #         self.send_flag = 1
    #         device = json.loads(event["text"])
    #         print(device["device"])
    #
    #         if (len(device["device"]) == 3):
    #             device_len = "04"
    #         else:
    #             device_len = "05"
    #
    #         enq = u"\u0005"
    #         etx = u"\u0004"
    #
    #         # receive된 명령어
    #         op = enq + "00WSS01" + device_len + "%" + device["device"] + "01" + etx
    #         print(" 삽입된 명령어 : " + op)
    #         try:
    #             if (self.ser.isOpen() == False):
    #                 print("Port is not Open")
    #             else:
    #                 self.ser.write(bytearray(op, 'ascii'))
    #                 self.send_flag = 0
    #                 self.ser.readline()
    #                 await asyncio.sleep(0.05)
    #         except Exception as e:
    #             print(e)

    async def websocket_disconnect(self, event):
        print("serial end")
        # self.ser.close()
        print("disconnected", event)
        raise StopConsumer()
