from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=list[schemas.Brand])
def read_brands(skip: int = 0, limit: int = 10, brand_name: str = None):
    db: Session = Depends(get_db)
    if brand_name is not None:
        return crud.get_brand(db, brand_name)    
    return crud.get_brands(db, skip, limit)


@app.get("/brand/{brand_name}", response_model=schemas.Brand)
def read_brand(brand_name: str):
    db: Session = Depends(get_db)
    return crud.get_brand(db, brand_name)

