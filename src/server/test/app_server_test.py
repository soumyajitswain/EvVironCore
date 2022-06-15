import asyncio
import websockets
# {"action":"Authorize", "user_id":"1234"}
async def hello():
    async with websockets.connect('ws://localhost:7000') as websocket:
        while True:
            name = input("Enter Sample request? ")
            await websocket.send(name)
            print("> {}".format(name))

            greeting = await websocket.recv()
            print("< {}".format(greeting))


asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()