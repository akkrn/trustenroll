from collections import defaultdict
from typing import List

from fastapi import Request
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from cache import CacheRoute
from models import Card, MainCategory, SubCategory, VisitLog
from schemas import (
    BankCardsSchema,
    CardSchema,
    MainCategoryDetailSchema,
    MainCategorySchema,
)
from service import extract_available
from user_agents import parse

api_router = APIRouter(route_class=CacheRoute)


def sorting_and_ordering_cards(cards):
    grouped = defaultdict(list)
    for card in cards:
        grouped[card.bank_name].append(card)

    def bank_sort_key(item):
        bank_name, card_list = item
        total_balance = sum(extract_available(c.card_name) for c in card_list)
        return (-len(card_list), -total_balance)  # минус для сортировки по убыванию

    sorted_grouped = sorted(grouped.items(), key=bank_sort_key)

    response = [
        {
            "bank_name": bank,
            "cards": sorted([CardSchema.from_orm(c) for c in card_list], key=lambda c: extract_available(c.card_name), reverse=True),
        }
        for bank, card_list in sorted_grouped
    ]
    return jsonable_encoder(response)


@api_router.get("/all_cards", response_model=List[BankCardsSchema])
async def get_all_cards_grouped():
    cards = await Card.all()
    response = sorting_and_ordering_cards(cards)
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
        return await get_all_cards_grouped()
    cards = await Card.filter(subcategory=subcategory)
    response = sorting_and_ordering_cards(cards)
    return JSONResponse(content=response)


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

    sorted_cards = sorting_and_ordering_cards(cards)
    data = {
        "id": main_category.id,
        "name": main_category.name,
        "subcategories": subcategories,
        "cards": sorted_cards,
    }
    response = jsonable_encoder(data)
    return JSONResponse(content=response)


@api_router.post("/ping")
async def track_visit(request: Request):
    print(request.headers)
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    ip = x_forwarded_for.split(",")[0] if x_forwarded_for else request.client.host
    ua_string = request.headers.get("User-Agent", "")
    user_agent = parse(ua_string)
    await VisitLog.create(
        ip=ip,
        device=user_agent.device.family,
        os=user_agent.os.family,
        browser=user_agent.browser.family,
    )
    return {"status": "ok"}
