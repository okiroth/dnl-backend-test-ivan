from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=list[schemas.Brand])
def read_brands(skip: int = 0, limit: int = 2, db: Session = Depends(get_db)):
    db_res = crud.get_brands(db, skip=skip, limit=limit)
    return db_res


@app.get("/?brand={brand_name}", response_model=schemas.Brand)
def read_brand(brand_name: int, db: Session = Depends(get_db)):
    db_res = crud.get_brand(db, brand_name=brand_name)
    if db_res is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    return db_res

