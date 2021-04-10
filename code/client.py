#!/usr/bin/env python

# WS client example
import json
import asyncio
import websockets

async def hello():
    
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:

        p = {'msg': "hola", 'version': '1', 'support': '1'}

        await websocket.send(json.dumps(p))
        print("enviado")


asyncio.get_event_loop().run_until_complete(hello())