from ast import stmt
from datetime import date, datetime
from decimal import Decimal
import json
from time import mktime, struct_time, time
from unittest import result
from winreg import QueryInfoKey
from click import echo
import sqlalchemy
from sqlalchemy_db_check import Chargebox, ChargingProfile, Connector, ConnectorChargingProfile, ConnectorMeterValue, ConnectorStatus, TransactionStart, TransactionStop, TransactionStopFail, Users
from sqlalchemy.orm import sessionmaker, Session
 


engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:root@127.0.0.1:3306/environ", echo=True, pool_size=20, max_overflow=0)

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

class UserDbFunc:
    def __init__(self, _user_id):
        self._user_id = _user_id

    def _get_user_by_id(_user_id, input):
        session = Session()
        stmt = sqlalchemy.select(Users).where(Users.user_id == _user_id)

        print(stmt)
        res = session.execute(stmt)

        user = ''
        _result = ''

        for r in res.scalars():
           print(str(r))
           user = r.__dict__
           user.pop('_sa_instance_state')
           print(user)

        x = {'action':input['action'], 'val':[user]}           
        _result = json.dumps(x)

        print(_result)
        return _result

class ChargeBoxFunc:
    def get_all_charge_box(input):
        session = Session()
        stmt = sqlalchemy.select(Chargebox).where(Chargebox.fw_update_status == 'Y')
        res = session.execute(stmt)
        list = []
        for row in res.scalars():
            r = row.__dict__
            #print(r)
            r.pop('_sa_instance_state')
            list.append(r)
        
        x = {'action':input['action'], 'func':input['func'], 'val':list} 
        _result = json.dumps(x, cls=CustomJsonEncoder)
        print(_result)
        return _result

    def get_charge_connector_detail_by_id(input):
        session = Session()
        join_query = session.query(Chargebox, Connector, ConnectorStatus )\
            .join(Connector, Connector.charge_box_id == Chargebox.charge_box_id)\
            .join(ConnectorStatus, ConnectorStatus.connector_pk == Connector.connector_pk)\
            .filter(Chargebox.charge_box_id == input['charge_box_id']).all()
        list = []
        for chargebox, connector, connector_status in join_query:
            r = str(chargebox.charge_box_pk)
            rowl = []
            cb = chargebox.__dict__
            cb.pop('_sa_instance_state')
            con = connector.__dict__
            con.pop('_sa_instance_state')
            cos = connector_status.__dict__
            cos.pop('_sa_instance_state')
            rowl.append(cb)
            rowl.append(con)
            rowl.append(cos)
            print(rowl)
            list.append(rowl)

        x = {'action':input['action'], 'func':input['func'], 'val':list}
        result = json.dumps(x, cls=CustomJsonEncoder)

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

    def get_transaction(input):
        session = Session()
        query = session.query(TransactionStart, TransactionStop, TransactionStopFail)\
            .join(TransactionStop, TransactionStart.transaction_pk == TransactionStop.transaction_pk)\
            .join(TransactionStopFail, TransactionStopFail.transaction_pk == TransactionStart.transaction_pk)\
            .filter(TransactionStart.transaction_pk == input['transaction_id']).all()    
        _list = []     
        for transactionStart, transactionStop, transactionStopFail in query:
            _ts1 = transactionStart.__dict__
            _ts1.pop('_sa_instance_state')
            _list.append(_ts1)

            _ts2 = transactionStop.__dict__
            _ts2.pop('_sa_instance_state')
            _list.append(_ts2)

            _ts3 = transactionStopFail.__dict__
            _ts3.pop('_sa_instance_state')
            _list.append(_ts3)

        x = {'action':input['action'], 'func':input['func'], 'val':_list}    
        result = json.dumps(x, cls=CustomJsonEncoder)
        return result    

    def get_transaction_by_connector_id(input):
        session = Session()
        query = session.query(TransactionStart, TransactionStop, TransactionStopFail)\
            .join(TransactionStop, TransactionStart.transaction_pk == TransactionStop.transaction_pk)\
            .join(TransactionStopFail, TransactionStopFail.transaction_pk == TransactionStart.transaction_pk)\
            .filter(TransactionStart.connector_pk == input['connector_pk']).all()

        _list = []     
        for transactionStart, transactionStop, transactionStopFail in query:
            _ts1 = transactionStart.__dict__
            _ts1.pop('_sa_instance_state')
            _list.append(_ts1)

            _ts2 = transactionStop.__dict__
            _ts2.pop('_sa_instance_state')
            _list.append(_ts2)

            _ts3 = transactionStopFail.__dict__
            _ts3.pop('_sa_instance_state')
            _list.append(_ts3)
            

        x = {'action':input['action'], 'func':input['func'], 'val':_list}    
        result = json.dumps(x, cls=CustomJsonEncoder)   
        return result    


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
        


                    