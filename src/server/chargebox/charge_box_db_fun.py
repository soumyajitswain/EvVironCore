from ast import stmt
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


class ChargingProfileFunc():
    def get_charging_profile_by_pk(input):
        session = Session()
        query = sqlalchemy.select(ChargingProfile).where(
            ChargingProfile.charging_profile_pk == input['charging_profile_pk'])

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

    def save_charging_profile(evse_id, charging_profile):
        session = Session()
        stmt = ChargingProfile(charging_profile_pk=evse_id,
                               stack_level=charging_profile['stack_level'],
                               charging_profile_purpose=charging_profile['charging_profile_purpose'],
                               charging_profile_kind=charging_profile['charging_profile_kind'],
                               recurrency_kind=charging_profile['recurrency_kind'],
                               valid_form=charging_profile['valid_form'],
                               valid_to=charging_profile['valid_to'],
                               duration_in_seconds=charging_profile['duration_in_seconds'],
                               start_schedule=charging_profile['start_schedule'],
                               charging_rate_unit=charging_profile['charging_rate_unit'],
                               min_charging_rate=charging_profile['min_charging_rate'],
                               desscription=charging_profile['description'],
                               note=charging_profile['note'])
        session.add(stmt)
        session.commit()
        session.close()

    def update_charging_profile(charging_profile):
        session = Session()
        session.query(ChargingProfile).\
            where(
                ChargingProfile.charging_profile_pk == charging_profile['charging_profile_pk']).\
            update(
                {ChargingProfile.charging_rate_unit: charging_profile['charging_rate_unit']})

        session.commit()
        session.close()

    def delete_charging_profile(charging_profile):
        session = Session()
        stmt = session.query(ChargingProfile).filter(
            ChargingProfile.charging_profile_pk == charging_profile['charging_profile_pk']).delete()
        session.commit()
        session.close()
