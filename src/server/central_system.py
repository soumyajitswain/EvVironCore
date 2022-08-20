from argparse import Action
import asyncio
import json
import logging
from datetime import datetime
import traceback
from unittest import result
from ocpp.v201.enums import AuthorizationStatusType, Action, RequestStartStopStatusType

from db_fun import TransactionManager as ts


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
            ts.update_transaction_status(
                self, charging_profile['transaction_id'], charging_profile['stack_level'])
        except Exception as e:
            print(e)
        return call_result.RequestStartTransactionPayload(
            status=RequestStartStopStatusType.accepted,
            transaction_id=str(remote_start_id)
        )

    @on(Action.RequestStopTransaction)
    def on_request_stop_transaction(self, transaction_id):
        print('Stop Transaction Request')
        _result = call_result.RequestStopTransactionPayload(
            status=RequestStartStopStatusType.accepted
        )
        try:
            tsDtl = ts.get_transaction_by_id(self, transaction_id)
            ts.stop_transaction(self, transaction_id, str(
                tsDtl['start_value']), 'Stopped')
        except Exception as e:
            print(traceback.format_exc())
            _result = call_result.RequestStopTransactionPayload(
                status=RequestStartStopStatusType.rejected
            )
        return _result

    @on(Action.GetTransactionStatus)
    def on_get_transaction_status(self, transaction_id):
        print('Get the transaction request')
        is_transaction_live = True
        try:
            input = {'action': 'GetTransactionStatus',
                     'func': 'get_transaction_status', 'transaction_id': transaction_id}
            tsDtl = ts.get_transaction(input)
            tsDtl = json.loads(tsDtl)
            if not tsDtl['val']:
                is_transaction_live = False

            _result = call_result.GetTransactionStatusPayload(
                messages_in_queue=is_transaction_live
            )

        except Exception as e:
            print(traceback.format_exc())
            _result = call_result.GetTransactionStatusPayload(
                messages_in_queue=is_transaction_live
            )
        return _result

    @on(Action.SetChargingProfile)
    def on_set_charging_profile(self, evse_id, charging_profile):
        print('Set Charging Profile ')

        try:
            _result = call_result.SetChargingProfilePayload(
                status='Accepted',
                status_info={"reasonCode": '200'}
            )

        except Exception as e:
            print(traceback.format_exc())

        return _result

    @on(Action.ClearChargingProfile)
    def on_clear_charging_profile(self, charging_profile_id, charging_profile_criteria):
        print('Clear Charge Profile')

        try:
            _result = call_result.ClearChargingProfilePayload(
                status='Unknown',
                status_info={
                    "reasonCode": "ABCDEFGHIJKLMNOPQ",
                    "customData": {
                        "vendorId": "ABCDEFGHIJK"
                    },
                    "additionalInfo": "ABCDEFGHIJKLMNO"
                }
            )

        except Exception as e:
            print(traceback.format_exc())

        return _result

    @on(Action.GetChargingProfiles)
    def on_get_charging_profiles(self, request_id, charging_profile, evse_id ):
        print('Get Charge Profiles')

        try:
            _result = call_result.GetChargingProfilesPayload(
                status="NoProfiles",
                status_info={
                    "reasonCode":"wewedw"
                }
            )

        except Exception as e:
            print(traceback.format_exc())

        return _result

    @on(Action.ReportChargingProfiles)
    def on_report_charging_profiles(self, request_id, charging_profile, evse_id, charging_limit_source, tbc ):
        print('report Charge Profiles')

        try:
            _result = call_result.ReportChargingProfilesPayload(

            )

        except Exception as e:
            print(traceback.format_exc())

        return _result

    @on(Action.ClearedChargingLimit)
    def on_cleared_charging_limit(self, charge_box_id ):
        print('Clear charging limit')
        try:
            _result = call_result.ClearedChargingLimitPayload()
        except Exception as e:
            print(traceback.format_exc())

        return _result

    @on(Action.ClearVariableMonitoring)
    def on_clear_variable_monitoring(self,id ):
        print('Clear charging limit')
        try:
            _result = call_result.ClearVariableMonitoringPayload()

        except Exception as e:
            print(traceback.format_exc())
            
        return _result

    @on(Action.CostUpdate)
    def on_cost_update(self):
        print('Cost update')
        try:
            _result = call_result.CostUpdatedPayload()
        except Exception as e:
            print(traceback.format_exc())
            
        return _result

    @on(Action.CustomerInformation)
    def on_customer_information(self):
        print('Customer information')
        try:
            _result = call_result.CustomerInformationPayload(
                status="NoProfiles",
                status_info={
                    "reasonCode":"wewedw"
                }
            )
        except Exception as e:
            print(traceback.format_exc())
            
        return _result

    @on(Action.CustomerInformation)
    def on_customer_information(self):
        print('Customer information')
        try:
            _result = call_result.CustomerInformationPayload(
                status="NoProfiles",
                status_info={
                    "reasonCode":"wewedw"
                }
            )
        except Exception as e:
            print(traceback.format_exc())
            
        return _result

    @on(Action.DataTransfer)
    def on_data_transfer(self, vendor_id, message_id, data):
        print('Data Transfer')
        try:
            _result = call_result.DataTransferPayload(
                status="NoProfiles",
                status_info={
                    "reasonCode":"wewedw"
                }
            )
        except Exception as e:
            print(traceback.format_exc())
            
        return _result

    @on(Action.DeleteCertificate)
    def on_delete_certificate(self, certificate_hash_data):
        print('Delete certificate')
        try:
            _result = call_result.DeleteCertificatePayload(
               status="NoProfiles",
                status_info={
                    "reasonCode":"wewedw"
                }
            )
            
        except Exception as e:
            print(traceback.format_exc())
            
        return _result

    @on(Action.FirmwareStatusNotification)
    def on_firmware_status_notification(self, status, request_id):
        print('Firmware Status Notification')
        try:
            _result = call_result.FirmwareStatusNotificationPayload()
            
        except Exception as e:
            print(traceback.format_exc())
            
        return _result

    @on(Action.Get15118EVCertificate)
    def on_get_15118_ev_certificate(self, iso15118_schema_version, action, exi_request):
        print('Get 15118 EVcertificate')
        try:
            _result = call_result.Get15118EVCertificatePayload(
                status='Accepted',
                exiReponse='acaefwef',
                status_info={
                    'reasonCode':'asdcadcfw'
                }
            )
        except Exception as e:
            print(traceback.format_exc())
            
        return _result

    @on(Action.GetBaseReport)
    def on_get_base_report(self, rerquest_id, report_base):
        print('Get base report')
        try:
            _result = call_result.GetBaseReportPayload(
                status='Accepted',
                status_info={
                    'reasonCode':'asdcadcfw'
                }

            )
        except Exception as e:
            print(traceback.format_exc())
            
        return _result

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
