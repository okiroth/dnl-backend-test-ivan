from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=list[schemas.Brand])
def read_brands(
    db: Session = Depends(get_db),
    skip: int = 0, 
    limit: int = 10, 
    brand_name: str = ""
):
    return crud.get_brands(db, skip, limit, brand_name)


@app.get("/brand/{name}", response_model=schemas.Brand)
def read_brand(
    db: Session = Depends(get_db),
    name: str = ""
):
    return crud.get_brand(db, name)

