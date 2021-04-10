#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import json
import csv
import os

outputPath ="./server.csv"
async def hello(websocket, path):
    name = await websocket.recv()
    msg = json.loads(name)
    if not os.path.isfile(outputPath):
        with open(outputPath, 'w') as csvfile:
            fieldnames = ['msg', 'version', 'support']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(msg)
    else:
        with open(outputPath, 'a', newline='') as csvfile:
            fieldnames = ['msg', 'version', 'support']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(msg)


start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()