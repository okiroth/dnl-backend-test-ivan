from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    url = Column(String, unique=True)

    items = relationship("Category", back_populates="owner")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    url = Column(String, unique=True)

    brand_id = Column(Integer, ForeignKey("brand_id"))
    owner = relationship("Brand", back_populates="categories")


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    url = Column(String, unique=True)
    
    category_id = Column(Integer, ForeignKey("category_id"))
    owner = relationship("Category", back_populates="models")


class Model_Part(Base):
    __tablename__ = "model_parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    name = Column(String, unique=True)
    url = Column(String, unique=True)

    model_id = Column(Integer, ForeignKey("model_id"))
    owner = relationship("Model", back_populates="model_parts")
