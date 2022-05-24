import asyncio
from asyncio.log import logger
import logging
import websockets

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

        reply = 'Data received';

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

