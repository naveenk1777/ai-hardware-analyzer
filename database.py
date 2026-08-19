from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column,DateTime,Integer,String,Boolean
import datetime
impport os

databaseurl=os.getenv("DATABASE_URL")

engine=create_async_engine(databaseurl, echo=False)
Asyncsessionlocal= async_sessionmaker(engine , expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

class Sensortelemetry(Base):
    __tablename__= "Sensor_data"
    id= Column(Integer,primary_key=True,index=True)
    device_id=Column(String,index=True)
    batteryper=Column(Integer)
    irstus=Column(Boolean)
    timestamp=Column(DateTime, default=datetime.datetime.utcnow)
    
class Devicehealth():
    __tablename__="Device_health"
    id= Column(Integer,primary_key=True,index=True)
    device_id=Column(String,index=True)
    fault_detected=Column(Integer)
    fault_reason=Column(String)


