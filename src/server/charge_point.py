import asyncio
import logging

from requests import request

from ocpp.v201.datatypes import IdTokenType
from sqlalchemy import null


try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys
    sys.exit(1)


from ocpp.v20 import call
from ocpp.v20 import ChargePoint as cp

logging.basicConfig(level=logging.INFO)



class ChargePoint(cp):
   
    async def send_heartbeat(self, interval):
        request = call.HeartbeatPayload()
        while True:
            await self.call(request)
            await asyncio.sleep(interval)

    async def authorize_request(self):
        try:
            request = call.AuthorizePayload(
                id_token={
                 'id_token':'dcdcsadcsd',
                  'type':'ISO14443'
                }
            )

            response = await self.call(request)
            print(response)
            print(response.id_token_info)
            print(response.id_token_info['status'])
            if response.id_token_info['status'] == 'Accepted':
                print('Authorization successful')

        except KeyError:
            print('Exception while authorizing the request')

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charging_station={
                'model': 'Wallbox XYZ',
                'vendor_name': 'anewone'
            },
            reason="PowerUp"
        )
        response = await self.call(request)

        if response.status == 'Accepted':
            print("Connected to central system.")
            await self.send_heartbeat(response.interval)
            #await self.authorize_request()
            #response = await self.request_start_transaction_request()
            #transaction_id = response.transaction_id;
            #await self.request_stop_transaction_request(transaction_id);

    async def request_start_transaction_request(self):
        try:
            request = call.RequestStartTransactionPayload(
                id_token={
                 'id_token':'1234mee',
                  'type':'ISO14443'
                },
                remote_start_id=1233
                )

            response = await self.call(request)
            return response
        except KeyError:
            print('Exception')      

    async def request_stop_transaction_request(self, transactionId):
        try:
            request = call.RequestStopTransactionPayload(
                transaction_id=transactionId
                )

            response = await self.call(request)
        except KeyError as e:
            print('Exception in stop transaction')
            print(e)      

charge_point = null;
async def main():
    async with websockets.connect(
            'ws://localhost:9000/CP_1',
            subprotocols=['ocpp2.0.1']
    ) as ws:

        global charge_point
        charge_point = ChargePoint('CP_1', ws)
        await asyncio.gather(charge_point.start(),
                             charge_point.send_boot_notification())
    return charge_point

async def main_remote(charge_point):
    async with websockets.connect(
            'ws://localhost:9000/CP_1',
            subprotocols=['ocpp2.0.1']
    ) as ws:

        charge_point = ChargePoint('CP_1', ws)
        asyncio.gather(charge_point.start(),
                             charge_point.send_boot_notification())
    return charge_point

if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())
