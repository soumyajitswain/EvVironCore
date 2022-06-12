from abc import ABC, abstractmethod
import json

from sqlalchemy_db_check import Users
from db_fun import UserDbFunc as userdbfun


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