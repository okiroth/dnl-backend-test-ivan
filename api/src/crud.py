from sqlalchemy.orm import Session, joinedload

from . import models


def get_brand(db: Session, name):
    return (
        db.query(models.Brand)
        .filter(models.Brand.name == name)
        .options(
            joinedload(models.Brand.categories)
            .subqueryload(models.Category.models)
            .subqueryload(models.Model.parts)
        )
        .first()
    )


def get_brands(db: Session, skip, limit, brand_name):
    return (
        db.query(models.Brand)
        .filter(models.Brand.name.contains(brand_name)) 
        .offset(skip).limit(limit)
        .all()
    )



