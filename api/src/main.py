from fastapi.exceptions import ResponseValidationError
from fastapi.responses import PlainTextResponse
from fastapi import Depends, FastAPI, Query, Path
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


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse("Not found", status_code=200)


@app.get("/", response_model=list[schemas.Brand])
def brands_catalogue(
    db: Session = Depends(get_db),
    skip: int = 0, 
    limit: int = 10, 
    brand_name: str = Query("", description="Search if a Brand's name contains this string.")
):
    """
    Returns a list of Brands and their Categories.
    """
    return crud.get_brands(db, skip, limit, brand_name)


@app.get("/brand/{name}", response_model=schemas.Brand)
def brand_details(
    db: Session = Depends(get_db),
    name: str = Path(description="Exact name of the Brand.")
):
    """
    Returns a Brand and its Categories, Models and Parts.
    """
    return crud.get_brand(db, name)

