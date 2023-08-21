from sqlalchemy.orm import Session

from . import models, schemas


def get_brand(db: Session, brand_name: str):
    return db.query(models.Brand).filter(models.Brand.name == brand_name).first()


def get_brands(db: Session, skip: int = 0, limit: int = 2):
    return db.query(models.Brand).offset(skip).limit(limit).all()



