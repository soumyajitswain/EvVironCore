import asyncio
from asyncio.log import logger
import importlib
import json
import logging
import traceback
import websockets
from processinghub import HubInitializer as HubInitializer

# Create a handler for app message

async def handler(websocket, path):
    while True:
        try:
            data = await websocket.recv()
        except websocket.ConnectionClosed:
            print(f"Terminated")
            break

        logger.info(data)
        
        print(data)

        reply = 'ok'
        try:

            d = json.loads(str(data))
            
            print(d['action'])

            subClass = getattr(importlib.import_module("processinghub"), d['action'])

            hi = subClass(d)
            reply = hi.operation(d)

        except Exception:
            print('error processing the request')
            traceback.print_exc()
            reply='error'

        await websocket.send(reply)
        print(f"> {reply}")

async def main():
    #  deepcode ignore BindToAllNetworkInterfaces: <Example Purposes>
    server = await websockets.serve(
        handler,
        '0.0.0.0',
        7000
    )

    logging.info("Server Started listening to new connections...")
    await server.wait_closed()

if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())

