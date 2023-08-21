from sqlalchemy.orm import Session

from . import models, schemas


def get_brand(db: Session, brand_name):
    return db.query(models.Brand).filter(models.Brand.name == brand_name).first()


def get_brands(db: Session, skip, limit):
    return db.query(models.Brand).offset(skip).limit(limit).all()



