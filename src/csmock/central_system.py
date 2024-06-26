from argparse import Action
import asyncio
import logging
from datetime import datetime
from ocpp.v201.enums import AuthorizationStatusType, Action, RequestStartStopStatusType

from server.db_fun import TransactionManager as ts


try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys
    sys.exit(1)

from ocpp.routing import on
from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call_result

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    @on('BootNotification')
    def on_boot_notification(self, charging_station, reason, **kwargs):
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status='Accepted'
        )

    @on('Heartbeat')
    def on_heartbeat(self):
        print('Got a Heartbeat!')
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') + "Z"
        )
    
    @on(Action.Authorize)
    def on_authorize_request(self, id_token):
        print('Authorize Request!')
        return call_result.AuthorizePayload(
          id_token_info={"status": AuthorizationStatusType.accepted}
        )

    @on(Action.RequestStartTransaction)
    def on_request_start_transaction(self, id_token, remote_start_id, evse_id, charging_profile):
        print('Start Transaction Request')
        try:
            print(charging_profile)
            print(charging_profile['transaction_id'])
            print(charging_profile['stack_level'])
        except Exception as e:
            print(e)    
        return call_result.RequestStartTransactionPayload(
          status=RequestStartStopStatusType.accepted,
          transaction_id=str(remote_start_id)
        )

    @on(Action.RequestStopTransaction)
    def on_request_stop_transaction(self, transaction_id):
        print('Stop Transaction Request')
        return call_result.RequestStopTransactionPayload(
          status=RequestStartStopStatusType.accepted
        )

async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint
    instance and start listening for messages.
    """
    try:
        requested_protocols = websocket.request_headers[
            'Sec-WebSocket-Protocol']
    except KeyError:
        logging.info("Client hasn't requested any Subprotocol. "
                     "Closing Connection")
        return await websocket.close()
        logging.error(
            "Client hasn't requested any Subprotocol. Closing Connection"
        )
        return await websocket.close()
    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        # In the websockets lib if no subprotocols are supported by the
        # client and the server, it proceeds without a subprotocol,
        # so we have to manually close the connection.
        logging.warning('Protocols Mismatched | Expected Subprotocols: %s,'
                        ' but client supports %s | Closing connection',
                        websocket.available_subprotocols,
                        requested_protocols)
        return await websocket.close()

    charge_point_id = path.strip('/')
    charge_point = ChargePoint(charge_point_id, websocket)

    await charge_point.start()


async def main():
    #  deepcode ignore BindToAllNetworkInterfaces: <Example Purposes>
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp2.0.1']
    )

    logging.info("Server Started listening to new connections...")
    await server.wait_closed()


if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())
