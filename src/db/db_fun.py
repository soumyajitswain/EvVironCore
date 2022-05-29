import sqlalchemy
from db.sqlalchemy_db_check import Chargebox, Users as user
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
    def  _get_all_charge_box(self):
        session = Session()
        query = session.query(Chargebox).filter(ChargeBoxFunc.fw_update_status == 'N')
        _result = query.all
        return _result

        
        