from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models import Station, StationPatch
from app.db import get_db, init_db, SessionLocal
from sqlalchemy.orm import Session
from app.db_models import StationDB

app = FastAPI()

init_db()

STATIONS = []

@app.get('/health')
def health():
    return {"status": "ok"}

@app.post("/stations", status_code=201)
def post_stations(station: Station, db: Session = Depends(get_db)):
    station_db= StationDB(
        code=station.code,
        name=station.name,
        capacity=station.capacity,
        status=station.status,
    )
    db.add(station_db)

    try:
        db.commit()
        db.refresh(station_db)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="code already existing")

    return station_db
    

@app.get('/stations')
def get_station(status: str | None = None, db: Session = Depends(get_db)):
    if status is None:
        return db.execute(select(StationDB)).scalars().all()

    return db.execute(select(StationDB).where(StationDB.status == status)).scalars().all()

@app.get("/stations/{station_id}")
def get_station_by_id(station_id: int, db: Session = Depends(get_db)):
    station = db.execute(select(StationDB).where(StationDB.id == station_id)).scalar_one_or_none()
    if station is None:
        raise HTTPException(status_code=404, detail="station not found")
    return station

@app.patch("/stations/{station_id}")
def patch_station(station_id: int, data: StationPatch, db: Session = Depends(get_db)):
    station = db.execute(
        select(StationDB).where(StationDB.id == station_id)
    ).scalar_one_or_none()

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    changes = data.model_dump(exclude_unset=True)

    for key, value in changes.items():
        setattr(station, key, value)

    db.commit()
    db.refresh(station)

    return station