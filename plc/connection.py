from channels.generic.websocket import WebsocketConsumer
from channels.consumer import AsyncConsumer
import random
import serial
import asyncio
import json


class plcConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)


        await self.send({
            "type": "websocket.accept"
        });

        '''
        ser.write(bytearray(start1, 'ascii'))
        o = str(ser.readline())

        mx1 = o[13:17]
        mx2 = o[17:21]
        mx3 = o[21:25]
        mx4 = o[25:29]
        mx5 = o[29:33]
        mx6 = o[33:37]
        mx7 = o[37:41]
        '''
        await self.send({
            'type': 'websocket.send',
            # 'text': mx1+" | "+mx2+" | "+mx3+ " | "+mx4+" | "+mx5+" | " + mx6+ " | "+ mx7,
            'text': '통신중',
            })
        # self.accept()

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    async def websocket_receive(self, event):
        # await self.receive({
        #     "type" : "websocket.receive",
        # })
        print("receive", event)
