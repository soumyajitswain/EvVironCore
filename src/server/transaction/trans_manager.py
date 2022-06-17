import asyncio

from requests import request
import websockets

from ocpp.v20 import call

async def app_client(payload, charge_box_id):
    async with websockets.connect('ws://localhost:9000/'+str(charge_box_id),  
                                 subprotocols=['ocpp2.0.1']) as websocket:
         await websocket.send(payload)

         _result = await websocket.recv()

         return _result

async def request_start_transaction(self, id_token, charge_box_id, remote_start_id):
    try:
        request = call.RequestStartTransactionPayload(
            id_token={
                 'id_token':'dcdcsadcsd',
                  'type':'ISO14443'
                },
                remote_start_id=1233
        )
        response = await app_client(request, charge_box_id)
    except KeyError:
        print('Exception') 

async def request_stop_transaction(self, transaction_id):
    try:
        request = call.RequestStartTransactionPayload(
            id_token={
                 'id_token':'dcdcsadcsd',
                  'type':'ISO14443'
                },
                remote_start_id=1233
        )
        response = await app_client(request)
    except KeyError:
        print('Exception') 