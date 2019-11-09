import asyncio
import random
from channels.consumer import AsyncConsumer

class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

        while True:
            await asyncio.sleep(2)

            obj = random.random()
            # do_something (Ex: constantly query DB...)

            await self.send({
                'type': 'websocket.send',
                'text': obj,
            })

    async def websocket_receive(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        print("disconnected", event)
