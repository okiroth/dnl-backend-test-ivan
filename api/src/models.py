from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    url = Column(String, unique=True)

    categories = relationship("Category", back_populates="owner")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    url = Column(String, unique=True)

    brand_id = Column(Integer, ForeignKey("brands.id"))
    owner = relationship("Brand", back_populates="categories")

    models = relationship("Model", back_populates="owner", lazy='noload')


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    url = Column(String, unique=True)

    category_id = Column(Integer, ForeignKey("categories.id"))
    owner = relationship("Category", back_populates="models")

    parts = relationship("Part", back_populates="owner", lazy='noload')
    

class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    name = Column(String, unique=True)
    url = Column(String, unique=True)

    model_id = Column(Integer, ForeignKey("models.id"))
    owner = relationship("Model", back_populates="parts")
