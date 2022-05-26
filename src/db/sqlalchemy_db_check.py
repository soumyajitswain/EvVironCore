from lib2to3.pytree import Base
import sqlalchemy 
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:root@127.0.0.1:3306/environ")

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    first_name = sqlalchemy.Column(sqlalchemy.String(length=100))
    last_name = sqlalchemy.Column(sqlalchemy.String(length=100))
    birth_day = sqlalchemy.Column(sqlalchemy.DATE)
    sex = sqlalchemy.Column(sqlalchemy.CHAR)
    phone = sqlalchemy.Column(sqlalchemy.String(length=10))
    email = sqlalchemy.Column(sqlalchemy.String(length=50))
    note = sqlalchemy.Column(sqlalchemy.TEXT) 

class 
print(engine)

Base.metadata.create_all(engine)
