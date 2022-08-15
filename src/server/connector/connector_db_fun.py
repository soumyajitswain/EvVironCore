from ast import stmt
from cmath import phase
import os
import sys
from turtle import update
if os.path.dirname(os.path.abspath(__file__+"/../")) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__+"/../")))

from datetime import date, datetime
from decimal import Decimal
import json
from time import mktime, struct_time, time
from unittest import result
from winreg import QueryInfoKey
from click import echo
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_db_check import Chargebox, ChargingProfile, Connector, ConnectorChargingProfile, ConnectorMeterValue, ConnectorStatus, TransactionStart, TransactionStop, TransactionStopFail, Users, ChargeStationMessageQueue


engine = sqlalchemy.create_engine(
    "mariadb+mariadbconnector://root:root@127.0.0.1:3306/environ", echo=False, pool_size=100, max_overflow=10)

Session = sessionmaker(bind=engine)

session = Session()


class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return str(obj)
        if isinstance(obj, struct_time):
            return datetime.fromtimestamp(mktime(obj))
        return super(CustomJsonEncoder, self).default(obj)


class ConnectorFunc():
    def get_connector_by_pk(input):
        session = Session()
        query = session.query(Connector).filter(
            Connector.connector_pk == input['connector_pk']).\
            filter(Connector.charge_box_id == input['charge_box_id']).\
            filter(Connector.connector_id == input['connector_id'])

        list = []
        for row in query.all():
            r = row.__dict__
            r.pop('_sa_instance_state')
            list.append(r)

        x = {'action': input['action'], 'func': input['func'], 'val': list}
        _result = json.dumps(x, cls=CustomJsonEncoder)
        print(_result)
        session.close()
        return _result

    def save_connector(input):
        session = Session()
        stmt = Connector(connector_pk=input['connector_pk'],
                         charge_box_id=input['charge_box_id'],
                         connector_id=input['connector_id'])
        session.add(stmt)
        session.commit()
        session.close()

    def update_connector(input):
        session = Session()
        session.query(Connector).\
            where(
                Connector.connector_pk == input['connector_pk'])
        session.commit()
        session.close()

    def delete_charging_profile(input):
        session = Session()
        stmt = session.query(Connector).filter(
            Connector.connector_pk == input['connector_pk']).delete()
        session.commit()
        session.close()

class ConnectorChargingProfileFunc():
    def get_connector_by_pk(input):
        session = Session()
        query = session.query(ConnectorChargingProfile).filter(
            ConnectorChargingProfile.connector_pk == input['connector_pk']).\
            filter(ConnectorChargingProfile.connector_profile_pk == input['connector_profile_pk'])

        list = []
        for row in query.all():
            r = row.__dict__
            r.pop('_sa_instance_state')
            list.append(r)

        x = {'action': input['action'], 'func': input['func'], 'val': list}
        _result = json.dumps(x, cls=CustomJsonEncoder)
        print(_result)
        session.close()
        return _result

    def save_connector(input):
        session = Session()
        stmt = ConnectorChargingProfile(connector_pk=input['connector_pk'],
                         connector_profile_pk=input['connector_profile_pk']
        session.add(stmt)
        session.commit()
        session.close()

    def update_connector(input):
        session = Session()
        session.query(Connector).\
            where(
                ConnectorChargingProfile.connector_pk == input['connector_pk'])
        session.commit()
        session.close()

    def delete_charging_profile(input):
        session = Session()
        stmt = session.query(ConnectorChargingProfile).filter(
            Connector.connector_pk == input['connector_pk']).delete()
        session.commit()
        session.close()

class ConnectorMeterValueFunc():
    def get_connector_meter_value_by_pk(input):
        session = Session()
        query = session.query(ConnectorMeterValue).filter(
            ConnectorMeterValue.connector_pk == input['connector_pk']).\
            filter(ConnectorMeterValue.transaction_pk == input['transaction_profile_pk'])

        list = []
        for row in query.all():
            r = row.__dict__
            r.pop('_sa_instance_state')
            list.append(r)

        x = {'action': input['action'], 'func': input['func'], 'val': list}
        _result = json.dumps(x, cls=CustomJsonEncoder)
        print(_result)
        session.close()
        return _result

    def save_connector_meter_value(input):
        session = Session()
        stmt = ConnectorMeterValue(connector_pk=input['connector_pk'],
                         transaction_pk=input['transaction_pk'], value_timestamp=input['value_timestamp'],
                         value=input['value'], reading_context=input['reading_context'], 
                         format=input['format'], measureand=input['measureand'], location=input['location'],
                         unit=input['unit'], phase=input['phase']
        session.add(stmt)
        session.commit()
        session.close()

    def update_connector_meter_value(input):
        session = Session()
        session.query(Connector).\
            where(
                ConnectorMeterValue.connector_pk == input['connector_pk'])
        session.commit()
        session.close()

    def delete_charging_profile(input):
        session = Session()
        stmt = session.query(ConnectorMeterValue).filter(
            ConnectorMeterValue.connector_pk == input['connector_pk']).delete()
        session.commit()
        session.close()

class ConnectorStatusFunc():
    def get_connector_Status_by_pk(input):
        session = Session()
        query = session.query(ConnectorStatus).filter(
            ConnectorStatus.connector_pk == input['connector_pk'])
        list = []
        for row in query.all():
            r = row.__dict__
            r.pop('_sa_instance_state')
            list.append(r)

        x = {'action': input['action'], 'func': input['func'], 'val': list}
        _result = json.dumps(x, cls=CustomJsonEncoder)
        print(_result)
        session.close()
        return _result

    def save_connector_status(input):
        session = Session()
        stmt = ConnectorStatus(connector_pk=input['connector_pk'],
                         status_timestamp=input['status_timestamp'], status=input['status'],
                         error_code=input['error_code'], error_info=input['error_info'], 
                         vendor_id=input['vendor_id'], vendor_error_code=input['vendor_error_code'])
        session.add(stmt)
        session.commit()
        session.close()

    def update_connectorStatus(input):
        session = Session()
        session.query(Connector).\
            where(
                ConnectorStatus.connector_pk == input['connector_pk'])
        session.commit()
        session.close()

    def delete_connectorStatus(input):
        session = Session()
        stmt = session.query(ConnectorStatus).filter(
            ConnectorStatus.connector_pk == input['connector_pk']).delete()
        session.commit()
        session.close()
