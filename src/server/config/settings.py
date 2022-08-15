from ast import stmt
from cmath import phase
import os
import sys
from turtle import update

from ..sqlalchemy_db_check import Settings
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


class SettingsFunc():
    def get_settings_pk(input):
        session = Session()
        query = session.query(Settings).filter(
            Settings.installed_rank == input['installed_rank'])

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

    def save_settings(input):
        session = Session()
        stmt = Settings(app_id=input['app_id'],
                         heartbeat_interval_in_sec=input['heartbeat_interval_in_sec'],
                         hours_to_expire=input['hours_to_expire'],
                         mail_enabled=input['mail_enabled'],
                         mail_host=input['mail_host'],
                         mail_username=input['mail_username'],
                         mail_password= input['mail_password'],
                         mail_from=input['mail_from'],
                         mail_protocol=input['mail_protocol'],
                         mail_port=input['mail_port'],
                         mail_receipients=input['mail_receipients'],
                         notification_features=input['notification_features'])
        session.add(stmt)
        session.commit()
        session.close()

    def update_settings(input):
        session = Session()
        session.query(Settings).\
            where(
                Settings.app_id == input['aap_id'])
        session.commit()
        session.close()

    def delete_settings(input):
        session = Session()
        stmt = session.query(Settings).filter(
            Settings.app_id == input['app_id']).delete()
        session.commit()
        session.close()

