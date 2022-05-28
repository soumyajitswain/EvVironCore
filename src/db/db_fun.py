from requests import session
import sqlalchemy_db_check as sql

session = sql.session

class userdbfun:
    def _get_user_by_id(self):
        user = sql.User
        return user