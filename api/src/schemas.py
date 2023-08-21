from pydantic import BaseModel


class Base(BaseModel):
    name: str
    url: str

class Model_Parts(Base):
    id: int
    code: str
    class Config:
        orm_mode = True

class Model(Base):
    id: int
    model_parts: list[Model_Parts] = []
    class Config:
        orm_mode = True

class Category(Base):
    id: int
    brand_id: int
    models: list[Model] = []
    class Config:
        orm_mode = True

class Brand(Base):
    id: int
    categories: list[Category] = []
    class Config:
        orm_mode = True
