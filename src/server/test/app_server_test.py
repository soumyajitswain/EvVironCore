import asyncio
import websockets
# {"action":"Authorize", "user_id":"1234"}
# ChargeStation {"action":"ChargeStation", "user_id":"1234", "func":"GetAllChargeStations"}
# ChargeStation Connectors {"action":"ChargeStation", "user_id":"1234", "func":"ConnectorDetailByChargeBox", "charge_box_id":"1"}
# StartTransaction ChargeStation Connectors {"action":"StartTransaction", "user_id":"1234", "func":"start_transaction", "charge_box_id":"1"}
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