from ast import stmt
from cmath import phase
from doctest import script_from_examples
from ensurepip import version
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
from sqlalchemy_db_check import Chargebox, ChargingProfile, Connector, ConnectorChargingProfile, ConnectorMeterValue, ConnectorStatus, TransactionStart, TransactionStop, TransactionStopFail, Users, ChargeStationMessageQueue, SchemaVersion


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


class SchemaVersionFunc():
    def get_schema_version_pk(input):
        session = Session()
        query = session.query(SchemaVersion).filter(
            SchemaVersion.installed_rank == input['installed_rank'])

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

    def save_schema_version(input):
        session = Session()
        stmt = SchemaVersion(installed_rank=input['installed_rank'],
                         version=input['version'],
                         description=input['description'],
                         type=input['input'],
                         script=input['script'],
                         checksum=input['checksum'],
                         installed_by=input['installed_by'],
                         installed_on=input['intsalled_on'],
                         execution_time=input['execution_time'],
                         sucess=input['sucess'])
        session.add(stmt)
        session.commit()
        session.close()

    def update_schema_version(input):
        session = Session()
        session.query(SchemaVersion).\
            where(
                SchemaVersion.installed_rank == input['installed_rank'])
        session.commit()
        session.close()

    def delete_schema_version(input):
        session = Session()
        stmt = session.query(SchemaVersion).filter(
            SchemaVersion.installed_rank == input['installed_rank']).delete()
        session.commit()
        session.close()

