import asyncio
import json
import logging
import random
import traceback

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


from ocpp.v201 import call
from ocpp.v201 import ChargePoint as cp

from db_fun import ChargeBoxMessageQueueManager as msgqueue

logging.basicConfig(level=logging.INFO)


class ChargePointDBHelper():
    def get_all_message(self, action, func):
        list = msgqueue.get_message(
            self, action, func, 'N')
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
                for l in cp_db_helper.get_all_message('StartTransaction', 'start_transaction'):
                    response = await self.request_start_transaction_request(l['transaction_id'])
                    # cp_db_helper.update_message(l['message_id'], 'Y') # disabled for testing
                for r in cp_db_helper.get_all_message('StopTransaction', 'stop_transaction'):
                    response = await self.request_stop_transaction_request(r['transaction_id'])
                    # cp_db_helper.update_message(l['message_id'], 'Y') # disabled for testing
            except Exception as e:
                print(traceback.format_exc())

            await asyncio.sleep(interval)

    async def authorize_request(self):
        try:
            request = call.AuthorizePayload(
                id_token={
                    'id_token': 'dcdcsadcsd',
                    'type': 'ISO14443'
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
            # await self.authorize_request()
            # response = await self.request_start_transaction_request()
            #transaction_id = response.transaction_id;
            # await self.request_stop_transaction_request(transaction_id);

    async def request_start_transaction_request(self, transaction_id):
        try:
            charging_schedule = []
            """
            charging_schedule.append({
                        "id": 812,
                        "chargingRateUnit": "W",
                        "chargingSchedulePeriod": [
                            {
                                "startPeriod": 913,
                                "limit": 494.5,
                                "customData": {
                                    "vendorId": "ABCDEFGHIJKLMNO"
                                },
                                "numberPhases": 184,
                                "phaseToUse": 817
                            }
                        ],
                        "customData": {
                            "vendorId": "ABCDEFGHIJKLMNOPQRSTUVWXYZABC"
                        },
                        "startSchedule": "ABCDEFGHIJKLMNOPQRSTU",
                        "duration": 436,
                        "minChargingRate": 808.5,
                        "salesTariff": {
                            "id": 105,
                            "salesTariffEntry": [
                                {
                                    "relativeTimeInterval": {
                                        "start": 328,
                                        "customData": {
                                            "vendorId": "ABCDEFGH"
                                        },
                                        "duration": -60
                                    },
                                    "customData": {
                                        "vendorId": "ABCDEFGHIJKLMNOP"
                                    },
                                    "ePriceLevel": 440,
                                    "consumptionCost": [
                                        {
                                            "startValue": 231.0,
                                            "cost": [
                                                {
                                                    "costKind": "RenewableGenerationPercentage",
                                                    "amount": 687,
                                                    "customData": {
                                                        "vendorId": "ABCDEFGHIJKLMNOPQRSTUVWXYZA"
                                                    },
                                                    "amountMultiplier": -96
                                                }
                                            ],
                                            "customData": {
                                                "vendorId": "ABCDEFGHIJKLMNOPQR"
                                            }
                                        }
                                    ]
                                }
                            ],
                            "customData": {
                                "vendorId": "ABCDEFGHIJKLMNO"
                            },
                            "salesTariffDescription": "ABCDEFGHIJKLMNOPQRSTUVWXY",
                            "numEPriceLevels": 685
                        }
                    })
                    """
            charging_profile = json.dumps({
                "id": 761,
                "stackLevel": random.randint(1, 1000),
                "chargingProfilePurpose": "ChargingStationMaxProfile",
                "chargingProfileKind": "Recurring",
                "customData": {
                    "vendorId": "ABCDEFGHIJKLMNOPQRST"
                },
                "recurrencyKind": "Daily",
                "validFrom": "ABCDEFGHIJKLMNOPQRSTUVW",
                "validTo": "ABCDEFG",
                "transactionId": str(transaction_id)

            })
            print(charging_profile)
            request = call.RequestStartTransactionPayload(
                id_token={
                    'id_token': '1234mee',
                    'type': 'ISO14443'
                },
                remote_start_id=2,
                evse_id=2,
                charging_profile=json.loads(charging_profile)
            )

            response = await self.call(request)
            return response
        except Exception as e:
            print('Exception', e)
            print(traceback.format_exc())

    async def request_stop_transaction_request(self, transactionId):
        try:
            request = call.RequestStopTransactionPayload(
                transaction_id=str(transactionId)
            )

            response = await self.call(request)
        except KeyError as e:
            print(traceback.format_exc())
            print(e)


charge_point = null


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
