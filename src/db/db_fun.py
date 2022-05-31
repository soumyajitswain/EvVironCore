import json
from time import time
from winreg import QueryInfoKey
import sqlalchemy
from db.sqlalchemy_db_check import Chargebox, ChargingProfile, Connector, ConnectorChargingProfile, ConnectorMeterValue, ConnectorStatus, TransactionStart, TransactionStop, TransactionStopFail, Users as user
from sqlalchemy.orm import sessionmaker, Session

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:root@127.0.0.1:3306/environ")

Session = sessionmaker(bind=engine)

session = Session()

class UserDbFunc:
    def _get_user_by_id(self, _user_id):
        session = Session()
        query = session.query(user).filter(user.user_id == _user_id)
        user = query.get(0)
        return user

class ChargeBoxFunc:
    def get_all_charge_box(self):
        session = Session()
        query = session.query(Chargebox).filter(ChargeBoxFunc.fw_update_status == 'N')
        res = query.all
        _result = json.dumps([dict(r) for r in res])
        return _result

    def get_charge_connector_detail_by_id(self, charge_box_id):
        session = Session()
        join_query = session.query(Chargebox, Connector, ConnectorStatus )\
            .join(Connector, Connector.charge_box_id == Chargebox.charge_box_id)\
            .join(ConnectorStatus, ConnectorStatus.connector_pk == Connector.connector_pk)\
            .filter(Chargebox.charge_box_id == charge_box_id)
        
        result = json.dumps([dict(r) for r in join_query])

        return result

    def get_connector_status(self, connector_id):
        session = Session()
        query = session.query(ConnectorStatus).filter(ConnectorStatus.connector_pk == connector_id)
        _result = json.dumps([dict(r) for r in query.all])
        return _result


class TransactionManager:
    def start_transaction(self, connector_id, id_tag):
        session = Session()
        ts = TransactionStart(connector_pk = connector_id, id_tag = id_tag, start_timestamp = time.time(), event_timestamp = time.time(), start_value = '200')
        session.add(ts)
        session.commit()

    def stop_transaction(self, transaction_pk, stop_value, stop_reason):
        session = Session()
        ts = TransactionStop(transaction_pk = transaction_pk, \
            stop_value = stop_value, stop_reason = stop_reason, event_timestamp = time.time(), event_actor = 1)
        session.add(ts)
        session.commit()

    def get_transaction(self, transaction_id):
        session = Session()
        query = session.query(TransactionStart, TransactionStop, TransactionStopFail)\
            .join(TransactionStop, TransactionStart.transaction_pk == TransactionStop.transaction_pk)\
            .join(TransactionStopFail, TransactionStopFail.transaction_pk == TransactionStart.transaction_pk)
        res = query.all
        _result = json.dumps([dict(r) for r in res])

    def stop_fail_transaction(self, transaction_pk, stop_value, stop_reason, fail_reason):
        session = Session()
        ts = TransactionStop(transaction_pk = transaction_pk, \
          stop_value = stop_value, stop_reason = stop_reason, event_timestamp = time.time(), \
              event_actor = 1, fail_reason = fail_reason)
        session.add(ts)
        session.commit()

class ClassChargingMeasurement:
    def get_connector_value(self, connector_id):
        session = Session()
        query = session.query(ConnectorMeterValue).filter(ConnectorMeterValue.connector_pk == connector_id)
        _res = query.all()
        _result = json.dumps([dict(r) for r in _res])
        return _result

    def get_charging_profile(self, connector_id):
        session = Session()
        query = session.query(ConnectorChargingProfile, ChargingProfile).join(ConnectorChargingProfile, ConnectorChargingProfile.charging_profile_pk == ChargingProfile.charging_profile_pk)\
                .filter(ConnectorChargingProfile.connector_pk == connector_id)
        _res = query.all
        _result = json.dumps([dict(r) for r in _res])
        return _result               
        


                    