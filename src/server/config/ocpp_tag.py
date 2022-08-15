from ast import stmt
from cmath import phase
import os
import sys
from turtle import update

from ..sqlalchemy_db_check import OcppTag
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


class OcppTagFunc():
    def get_ocpp_tag_pk(input):
        session = Session()
        query = session.query(OcppTag).filter(
            OcppTag.ocpp_tag_pk == input['ocpp_tag_pk'])
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

    def save_ocpp_tag(input):
        session = Session()
        stmt = OcppTag(ocpp_tag_pk=input['ocpp_tag_pk'],
                         id_tag=input['id_tag'],
                         parent_id_tag=input['parent_id_tag'],
                         expiry_date=input['expiry_date'],
                         max_active_transaction_count=input['max_active_transaction_count'])
        session.add(stmt)
        session.commit()
        session.close()

    def update_ocpp_tag(input):
        session = Session()
        session.query(OcppTag).\
            where(
                OcppTag.ocpp_tag_pk == input['ocpp_tag_pk'])
        session.commit()
        session.close()

    def delete_ocpp_tag(input):
        session = Session()
        stmt = session.query(OcppTag).filter(
            OcppTag.ocpp_tag_pk == input['ocpp_tag_pk']).delete()
        session.commit()
        session.close()


