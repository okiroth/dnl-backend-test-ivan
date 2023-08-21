from sqlalchemy.orm import Session

from . import models, schemas


def get_brand(db: Session, name = ""):
    return (
        db.query(models.Brand)
        .filter(models.Brand.name == name)
        .first()
    )


def get_brands(db: Session, skip, limit, brand_name):
    return (
        db.query(models.Brand)
        .filter(models.Brand.name.contains(brand_name)) 
        .offset(skip).limit(limit)
        .all()
    ) 



