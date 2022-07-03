from abc import ABC, abstractmethod
import json

from sqlalchemy_db_check import Users
from db_fun import UserDbFunc as userdbfun, ChargeBoxFunc, TransactionManager


class HubInitializer(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def operation(self, _d):
        pass
        
    def serialize(self, data):
        d = self._action(data)
        _result = '';
        _result = globals()[d['action']].operation(d)
        
        return _result    

    def _action(self, data):
        d = json.load(data)
        return d

class Authorize(HubInitializer):
    def operation(self, _d):
        print('Authorize operation')
        _user_id = _d['user_id']
        print(_user_id)
        user = userdbfun._get_user_by_id(_user_id)
        _result = user
        print('Result sent')
        return _result

class ChargeStation(HubInitializer):
    def operation(self, _d):
        _user_id = _d['user_id']
        if _d['func'] == 'GetAllChargeStations':
            _result = ChargeBoxFunc.get_all_charge_box(_d)
            print('Get all Charge station detail')
        elif  _d['func'] == 'ConnectorDetailByChargeBox':
            charge_box_id = _d['charge_box_id']
            _result = ChargeBoxFunc.get_charge_connector_detail_by_id(_d)
        return _result

class StartTransaction(HubInitializer):
    def operation(self, _d):
        _user_id = _d['user_id']
        _result = ''
        if _d['func'] == 'start_transaction':
            charge_box_id = _d['charge_box_id']
            connector_pk = _d['connector_pk']
            _result = TransactionManager.get_transaction_by_connector_id(connector_pk)
        elif _d['func'] == 'transaction_status':
            transaction_id = _d['transaction_id']
            _result = TransactionManager.get_transaction(transaction_id)

        return _result      

        print('Authorize operation')

class StopTransaction(HubInitializer):
    def operation(self, data):
        print('Authorize operation')

class TransactionStatus(HubInitializer):
    def operation(self, data):
        print('Authorize operation')
