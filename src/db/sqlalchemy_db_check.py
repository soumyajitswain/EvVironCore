from cmath import phase
from email.headerregistry import Address
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

class Address(Base):
    __tablename__ = 'address'
    address_pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    street = sqlalchemy.Column(sqlalchemy.String(length=100))
    house_number = sqlalchemy.Column(sqlalchemy.String(length=100))
    zip_code = sqlalchemy.Column(sqlalchemy.DATE)
    city = sqlalchemy.Column(sqlalchemy.CHAR)
    country = sqlalchemy.Column(sqlalchemy.String(length=10))

class Chargebox(Base):
    __tablename__ = 'charge_box'
    charge_box_pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    charge_box_id = sqlalchemy.Column(sqlalchemy.String(length=100))
    endpoint_address = sqlalchemy.Column(sqlalchemy.String(length=100))
    ocpp_protocol = sqlalchemy.Column(sqlalchemy.String(length=10))
    registration_status = sqlalchemy.Column(sqlalchemy.String(length=10))
    charge_point_vendor = sqlalchemy.Column(sqlalchemy.String(length=10))
    charge_point_model = sqlalchemy.Column(sqlalchemy.String(length=10))
    charge_point_serial_number = sqlalchemy.Column(sqlalchemy.String(length=10))
    fw_version = sqlalchemy.Column(sqlalchemy.String(length=10))
    fw_update_status = sqlalchemy.Column(sqlalchemy.String(length=10))
    fw_update_timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    iccid = sqlalchemy.Column(sqlalchemy.String(length=10))
    imsi = sqlalchemy.Column(sqlalchemy.String(length=10))
    meter_type = sqlalchemy.Column(sqlalchemy.String(length=10))
    meter_serial_number = sqlalchemy.Column(sqlalchemy.String(length=10))
    diagnostics_status = sqlalchemy.Column(sqlalchemy.String(length=10))
    diagnostics_timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    last_heartbeat_timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    description = sqlalchemy.Column(sqlalchemy.TEXT)
    note = sqlalchemy.Column(sqlalchemy.TEXT)
    location_latitude = sqlalchemy.Column(sqlalchemy.DECIMAL)
    location_longitude = sqlalchemy.Column(sqlalchemy.DECIMAL)
    admin_address = sqlalchemy.Column(sqlalchemy.String(length=255))
    insert_connector_status = sqlalchemy.Column(sqlalchemy.INT)
    

class ChargingProfile(Base):
    __tablename__ = 'charging_profile'
    charging_profile_pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    stack_level = sqlalchemy.Column(sqlalchemy.INT)
    charging_profile_purpose = sqlalchemy.Column(sqlalchemy.String(length=100))
    charging_profile_kind = sqlalchemy.Column(sqlalchemy.String(length=10))
    recurrency_kind = sqlalchemy.Column(sqlalchemy.String(length=10))
    valid_form = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    valid_to = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    duration_in_seconds = sqlalchemy.Column(sqlalchemy.INT)
    start_schedule = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    charging_rate_unit = sqlalchemy.Column(sqlalchemy.String(length=10))
    min_charging_rate = sqlalchemy.Column(sqlalchemy.DECIMAL)
    description = sqlalchemy.Column(sqlalchemy.String(length=255))
    note = sqlalchemy.Column(sqlalchemy.TEXT)

class ChargingSchedulePeriod(Base):
    __tablename__ = 'charging_schedule_period'
    charging_profile_pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    start_period_in_seconds = sqlalchemy.Column(sqlalchemy.INT)
    power_limit = sqlalchemy.Column(sqlalchemy.DECIMAL)
    number_phases = sqlalchemy.Column(sqlalchemy.INT)

class Connector(Base):
    __tablename__ = 'connector'
    connector_pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    charge_box_id = sqlalchemy.Column(sqlalchemy.INT)
    connector_id = sqlalchemy.Column(sqlalchemy.DECIMAL)


class ConnectorChargingProfile(Base):
    __tablename__ = 'connector_charging_profile'
    connector_pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    charging_profile_pk = sqlalchemy.Column(sqlalchemy.INT)

class ConnectorMeterValue(Base):
    __tablename__ = 'connector_mater_value'
    connector_pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    transaction_pk = sqlalchemy.Column(sqlalchemy.INT)
    value_timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    value = sqlalchemy.Column(sqlalchemy.String(length=100))
    reading_context = sqlalchemy.Column(sqlalchemy.String(length=100))
    format = sqlalchemy.Column(sqlalchemy.String(length=100))
    measurand = sqlalchemy.Column(sqlalchemy.String(length=10))
    location = sqlalchemy.Column(sqlalchemy.String(length=100))
    unit = sqlalchemy.Column(sqlalchemy.String(length=255))
    phase = sqlalchemy.Column(sqlalchemy.String(length=100))

class ConnectorStatus(Base):
    __tablename__ = 'connector_status'
    connector_pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    status_timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    status = sqlalchemy.Column(sqlalchemy.String(length=255))
    error_code = sqlalchemy.Column(sqlalchemy.String(length=100))
    error_info = sqlalchemy.Column(sqlalchemy.String(length=100))
    vendor_id = sqlalchemy.Column(sqlalchemy.String(length=100))
    vendor_error_code = sqlalchemy.Column(sqlalchemy.String(length=10))

class OcppTag(Base):
    __tablename__ = 'ocpp_tag'
    ocpp_tag_pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_tag = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    parent_id_tag = sqlalchemy.Column(sqlalchemy.String(length=255))
    expiry_date = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    max_active_transaction_count = sqlalchemy.Column(sqlalchemy.INT)
    note = sqlalchemy.Column(sqlalchemy.TEXT)

class Reservation(Base):
    __tablename__ = 'reservation'
    reservation_pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    connector_pk = sqlalchemy.Column(sqlalchemy.Integer)
    transaction_pk = sqlalchemy.Column(sqlalchemy.Integer)
    id_tag = sqlalchemy.Column(sqlalchemy.String(length=255))
    start_datetime = sqlalchemy.Column(sqlalchemy.DATETIME)
    expiry_datetime = sqlalchemy.Column(sqlalchemy.DATETIME)
    status = sqlalchemy.Column(sqlalchemy.String(length=255))

class SchemaVersion(Base):
    __tablename__ = 'schema_version'
    installed_rank = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    version = sqlalchemy.Column(sqlalchemy.Integer)
    description = sqlalchemy.Column(sqlalchemy.Integer)
    type = sqlalchemy.Column(sqlalchemy.String(length=255))
    script = sqlalchemy.Column(sqlalchemy.DATETIME)
    checksum = sqlalchemy.Column(sqlalchemy.DATETIME)
    installed_by = sqlalchemy.Column(sqlalchemy.String(length=255))
    installed_on = sqlalchemy.Column(sqlalchemy.DATETIME)
    execution_time = sqlalchemy.Column(sqlalchemy.DATETIME)
    sucess = sqlalchemy.Column(sqlalchemy.String(length=255))

class Settings(Base):
    __tablename__ = 'settings'
    app_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    heartbeat_interval_in_sec = sqlalchemy.Column(sqlalchemy.Integer)
    hours_to_expire = sqlalchemy.Column(sqlalchemy.Integer)
    mail_enabled = sqlalchemy.Column(sqlalchemy.String(length=255))
    mail_host = sqlalchemy.Column(sqlalchemy.DATETIME)
    mail_username = sqlalchemy.Column(sqlalchemy.DATETIME)
    mail_password = sqlalchemy.Column(sqlalchemy.String(length=255))
    mail_from = sqlalchemy.Column(sqlalchemy.DATETIME)
    mail_protocol = sqlalchemy.Column(sqlalchemy.DATETIME)
    mail_port = sqlalchemy.Column(sqlalchemy.String(length=255))
    mail_receipients = sqlalchemy.Column(sqlalchemy.DATETIME)
    notification_features = sqlalchemy.Column(sqlalchemy.String(length=255))

class TransactionStart(Base):
    __tablename__ = 'transaction_start'
    transaction_pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    event_timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    connector_pk = sqlalchemy.Column(sqlalchemy.Integer)
    id_tag = sqlalchemy.Column(sqlalchemy.String(length=255))
    start_timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    start_value = sqlalchemy.Column(sqlalchemy.String(length=255))

class TransactionStop(Base):
    __tablename__ = 'transaction_stop'
    transaction_pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    event_timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    event_actor = sqlalchemy.Column(sqlalchemy.Integer)
    stop_timestamp = sqlalchemy.Column(sqlalchemy.String(length=255))
    stop_value = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    stop_reason = sqlalchemy.Column(sqlalchemy.String(length=255))

class TransactionStopFail(Base):
    __tablename__ = 'transaction_stop_failed'
    transaction_pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    event_timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    event_actor = sqlalchemy.Column(sqlalchemy.Integer)
    stop_timestamp = sqlalchemy.Column(sqlalchemy.String(length=255))
    stop_value = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    stop_reason = sqlalchemy.Column(sqlalchemy.String(length=255))
    fail_reason = sqlalchemy.Column(sqlalchemy.TEXT)

print(engine)

Base.metadata.create_all(engine)
