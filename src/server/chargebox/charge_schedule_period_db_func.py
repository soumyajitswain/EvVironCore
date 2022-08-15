from ast import stmt
import os
import sys
from turtle import update

from ..sqlalchemy_db_check import ChargingSchedulePeriod, Reservation
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


class ChargingSchedulePeriodFunc():
    def get_charging_schedule_period_by_id(input):
        session = Session()
        query = sqlalchemy.select(ChargingSchedulePeriod).where(
            ChargingSchedulePeriod.charging_profile_pk == input['charging_profile_pk'])

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

    def save_charging_schedule_period(input):
        session = Session()
        stmt = ChargingSchedulePeriod(charging_profile_pk=input['charging_profile_pk'],
                                      start_period_in_seconds=input['start_period_in_seconds'],
                                      charging_profile_purpose=input['charging_profile_purpose'],
                                      power_limit=input['power_limit'],
                                      number_phases=input['number_phases'])
        session.add(stmt)
        session.commit()
        session.close()

    def update_charging_schedule_period(input):
        session = Session()
        session.query(ChargingSchedulePeriod).\
            where(
                ChargingSchedulePeriod.charging_profile_pk == input['charging_profile_pk']).\
            update(
                {ChargingSchedulePeriod.number_phases: input['number_phases']})

        session.commit()
        session.close()

    def delete_charging_profile(input):
        session = Session()
        stmt = session.query(ChargingSchedulePeriod).filter(
            ChargingSchedulePeriod.charging_profile_pk == input['charging_profile_pk']).delete()
        session.commit()
        session.close()

class ReservationFunc():
    def get_reservation(input):
        session = Session()
        query = sqlalchemy.select(Reservation).where(
            Reservation.reservation_pk == input['reservation_pk'])

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

    def save_reservation(input):
        session = Session()
        stmt = Reservation(registry=input['registry'],
                                      start_period_in_seconds=input['start_period_in_seconds'],
                                      charging_profile_purpose=input['charging_profile_purpose'],
                                      power_limit=input['power_limit'],
                                      number_phases=input['number_phases'])
        session.add(stmt)
        session.commit()
        session.close()

    def update_reservation(input):
        session = Session()
        session.query(Reservation).\
            where(
                Reservation.reservation_pk == input['reservation_pk']).\
            update(
                {Reservation.expiry_datetime: input['expiry_datetime']})

        session.commit()
        session.close()

    def delete_reservation(input):
        session = Session()
        stmt = session.query(Reservation).filter(
            Reservation.reservation_pk == input['reservation_pk']).delete()
        session.commit()
        session.close()
