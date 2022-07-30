import asyncio
import json
import logging
import random

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

from db_fun import ChargeBoxMessageQueueManager as msgqueue

logging.basicConfig(level=logging.INFO)

class ChargePointDBHelper():
    def get_all_message(self):
       list = msgqueue.get_message(self, 'StartTransaction', 'start_transaction', 'N')
       return list

    def update_message(self, message_id, status):
        msgqueue.update_message(self, message_id, status)   

cp_db_helper = ChargePointDBHelper()

class ChargePoint(cp):
   
    async def send_heartbeat(self, interval):
        request = call.HeartbeatPayload()
        while True:
            await self.call(request)
            try:
                for l in cp_db_helper.get_all_message():
                    response = await self.request_start_transaction_request(l['transaction_id'])
                    #cp_db_helper.update_message(l['message_id'], 'Y')
            except Exception as e:
                print(e)    
            
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

    async def request_start_transaction_request(self, transaction_id):
        try:
            chargingSchedulePeriod = [{'start_period':1, 'limit':10}]
            chargingSchedule = json.dumps([{'id':1, 'chargingRateUnit':'A','chargingSchedulePeriod':chargingSchedulePeriod }])
            charging_profile = {'id':2,'stackLevel': random.randint(0, 1000),'chargingSchedule':json.loads(chargingSchedule),'chargingProfilePurpose':'TxDefaultProfile', 'chargingProfileKind':'Absolute'}
            request = call.RequestStartTransactionPayload(
                id_token={
                 'id_token':'1234mee',
                  'type':'ISO14443'
                },
                remote_start_id=2
                )

            response = await self.call(request)
            return response
        except KeyError as e:
            print('Exception', e)      

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
