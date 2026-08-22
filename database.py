from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column,DateTime,Integer,String,Boolean
import datetime
import os

databaseurl=os.getenv("DATABASE_URL")

engine=create_async_engine(databaseurl, echo=False)
Asyncsessionlocal= async_sessionmaker(engine , expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

class Sensortelemetry(Base):
    __tablename__= "Sensor_data_v2"
    id= Column(Integer,primary_key=True,index=True)
    device_id=Column(String,index=True)
    battery_percent=Column(Integer)
    ir_status=Column(Boolean)
    timestamp=Column(DateTime, default=datetime.datetime.utcnow)
    
class Devicehealth(Base):
    __tablename__="Device_health_v2"
    id= Column(Integer,primary_key=True,index=True)
    device_id=Column(String,index=True)
    fault_detected=Column(Boolean)
    fault_reason=Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


