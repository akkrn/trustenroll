from collections import defaultdict
from typing import List


from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from cache import CacheRoute
from models import Card, MainCategory, SubCategory
from schemas import (
    BankCardsSchema,
    CardSchema,
    MainCategoryDetailSchema,
    MainCategorySchema,
)

api_router = APIRouter(route_class=CacheRoute)


@api_router.get("/all_cards", response_model=List[BankCardsSchema])
async def get_all_cards_grouped():
    cards = await Card.all()
    grouped = defaultdict(list)

    for card in cards:
        grouped[card.bank_name].append(card)
    response = [
        {
            "bank_name": bank,
            "cards": [CardSchema.from_orm(c) for c in card_list],
        }
        for bank, card_list in grouped.items()
    ]
    response = jsonable_encoder(response)
    return JSONResponse(content=response)


@api_router.get("/main_categories", response_model=List[MainCategorySchema])
async def get_main_categories():
    return await MainCategory.all()


@api_router.get(
    "/cards/by_subcategory/{subcategory_id}/cards",
    response_model=List[CardSchema],
)
async def get_cards_by_subcategory(subcategory_id: int):
    subcategory = await SubCategory.get_or_none(id=subcategory_id)
    if not subcategory:
        return await Card.all()
    return await Card.filter(subcategory=subcategory)


@api_router.get(
    "/main_categories/{main_category_id}/details",
    response_model=MainCategoryDetailSchema,
)
async def get_main_category_details(main_category_id: int):
    main_category = await MainCategory.get_or_none(id=main_category_id)
    if not main_category:
        raise HTTPException(status_code=404, detail="Main category not found")
    subcategories = await SubCategory.filter(main_category=main_category).select_related("main_category")
    subcategory_ids = [sub.id for sub in subcategories]
    cards = await Card.filter(subcategory_id__in=subcategory_ids)
    return {
        "id": main_category.id,
        "name": main_category.name,
        "subcategories": subcategories,
        "cards": cards,
    }
