from abc import ABC, abstractmethod
import json

import src.db.sqlalchemy_db_check as sqlalchemy_db_check
from src.db.db_fun import UserDbFunc as userdbfun

class HubInitializer(ABC):

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
        _user_id = _d.user_id
        user = userdbfun._get_user_by_id(_user_id)
        _result = user
        print('Authorize operation')
        return _result

class ChargeStation(HubInitializer):
    def operation(self, _d):
        _user_id = _d.user_id
        if _d.action == 'get_all':
            charge_station_all = userdbfun._get_user_by_id(_user_id)
            _result = charge_station_all
        print('Get all Charge station detail')
        return _result

class StartTransaction(HubInitializer):
    def operation(self, data):
        print('Authorize operation')

class StopTransaction(HubInitializer):
    def operation(self, data):
        print('Authorize operation')

class TransactionStatus(HubInitializer):
    def operation(self, data):
        print('Authorize operation')
