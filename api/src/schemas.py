from typing import Optional
from pydantic import BaseModel, ConfigDict



class Base(BaseModel):
    name: str
    url: str


class Parts(Base):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: Optional[str] = None

class Model(Base):
    model_config = ConfigDict(from_attributes=True)
    id: int
    parts: list[Parts]

class Category(Base):
    model_config = ConfigDict(from_attributes=True)
    id: int
    models: list[Model]

class Brand(Base):
    model_config = ConfigDict(from_attributes=True)
    id: int
    categories: list[Category]