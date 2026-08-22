from fastapi import FastAPI,Depends
from typing import Annotated
from pydantic import BaseModel,Field
from sqlalchemy import future
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base,engine,Asyncsessionlocal,Sensortelemetry,Devicehealth
from contextlib import asynccontextmanager
from sqlalchemy.future import select
from analyzewithai import analyzewithai



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

@app.post("/api/telemetry")
async def ingestdata(payload:telemetrypayload,db:dbsession):
    new_record=Sensortelemetry(device_id=payload.device_id,batteryper=payload.batteryper,irstus=payload.irstus)
    db.add(new_record)
    await db.commit()
    return {"status": "ok", "message": "sensor data entered in database"}


@app.post("/api/diagnose/{device_id}")
async def run_diagnostics(device_id:str,db:dbsession):
    query=(
    select(Sensortelemetry)
    .where(Sensortelemetry.device_id == device_id)
    .order_by(Sensortelemetry.id.desc())
    )
    result=await db.execute(query)
    telemetry=result.scalars().all()
    formatted_data = [
        {"device_id": d.device_id, "battery": d.batteryper, "irstus": d.irstus} 
        for d in telemetry
    ]
    print("Sending telemetry to AI for analysis...")

    ai_verdict = analyzewithai(formatted_data)

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
    

