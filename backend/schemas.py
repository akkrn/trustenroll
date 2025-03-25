from typing import List

from pydantic import BaseModel


class CardSchema(BaseModel):
    id: int
    bank_name: str
    card_name: str

    class Config:
        from_attributes = True


class MainCategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class SubCategorySchema(BaseModel):
    id: int
    name: str
    main_category: MainCategorySchema

    class Config:
        from_attributes = True


class BankCardsSchema(BaseModel):
    bank_name: str
    cards: List[CardSchema]


class MainCategoryDetailSchema(BaseModel):
    id: int
    name: str
    subcategories: List[SubCategorySchema]
    cards: List[CardSchema]

    class Config:
        orfrom_attributesm_mode = True
