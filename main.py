from fastapi import FastAPI,Depends,HTTPException,Security
from fastapi.security import APIKeyHeader
from typing import Annotated
from pydantic import BaseModel,Field
from sqlalchemy import future
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base,engine,Asyncsessionlocal,Sensortelemetry,Devicehealth
from contextlib import asynccontextmanager
from sqlalchemy.future import select
from analyzewithai import analyzewithai
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name="X-Hardware-Key")

def verify_hardware_key(api_key: str = Security(api_key_header)):
    expected_key = os.getenv("HARDWARE_API_KEY") 
    if not expected_key or api_key != expected_key:
        logger.warning("Unauthorized access attempt blocked!")
        raise HTTPException(status_code=401, detail="Invalid Hardware API Key")

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app=FastAPI(title="iot predictive cloud bridge",lifespan=lifespan)

async def get_db():
    async with Asyncsessionlocal() as session:
        yield session

dbsession=Annotated[AsyncSession, Depends(get_db)]

class telemetrypayload(BaseModel):
    device_id:str
    batteryper:int = Field(ge=0, le=100)
    irstus:bool

@app.post("/api/telemetry", dependencies=[Depends(verify_hardware_key)])
async def ingestdata(payload:telemetrypayload,db:dbsession):
    new_record=Sensortelemetry(
        device_id=payload.device_id,
        battery_percent=payload.battery_percent,
        ir_status=payload.ir_status
    )
    db.add(new_record)
    await db.commit()
    logger.info(f"Telemetry saved for {payload.device_id}") 
    return {"status": "ok", "message": "sensor data entered in database"}


@app.post("/api/diagnose/{device_id}")
async def run_diagnostics(device_id:str,db:dbsession):
    try:
        query=(
        select(Sensortelemetry)
        .where(Sensortelemetry.device_id == device_id)
        .order_by(Sensortelemetry.id.desc())
        .limit(100)
        )
        result=await db.execute(query)
        telemetry=result.scalars().all()
    
        if not telemetry:
                raise HTTPException(status_code=404, detail="No telemetry data found for this device.")
        
        formatted_data = [
            {"device_id": d.device_id, "battery": d.batteryper, "irstus": d.irstus} 
            for d in telemetry
        ]
        print("Sending telemetry to AI for analysis...")
    
        ai_verdict = await analyzewithai(formatted_data)
    
        health_record = Devicehealth(
            device_id=device_id,
            fault_detected=ai_verdict.fault_detected,
            fault_reason=ai_verdict.fault_reason
        )
        db.add(health_record)
        await db.commit()
        
        return {
            "ai_diagnosis": ai_verdict,
            "data_points_analyzed": len(formatted_data),
            "raw_data": formatted_data
        }

    except Exception as e:
        print(f"Error during diagnostics: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during diagnosis.")

