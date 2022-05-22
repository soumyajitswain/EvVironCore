import asyncio
from asyncio.log import logger
import logging
import websockets

# Create a handler for app message

async def handler(websocket, path):
    data = await websocket.recv()

    logger.info(data)
    
    print(data)

    reply = 'Data received';

    await websocket.send(reply)

async def main():
    #  deepcode ignore BindToAllNetworkInterfaces: <Example Purposes>
    server = await websockets.serve(
        handler,
        '0.0.0.0',
        8000
    )

    logging.info("Server Started listening to new connections...")
    await server.wait_closed()

if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())

