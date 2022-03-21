import aiohttp as aiohttp
from fastapi import APIRouter

from app.hyuabot.kakao.core.config import AppSettings
from app.hyuabot.kakao.core.create_response import create_carousel_response
from app.hyuabot.kakao.core.parse_input import parse_user_utterance
from app.hyuabot.kakao.scheme.request import KakaoRequest
from app.hyuabot.kakao.scheme.response import ServerResponse, TextCard

food_restaurant_router = APIRouter(prefix="/restaurant", tags=["Restaurant menu by campus"])


async def fetch_menu_list_by_campus() -> list:
    app_settings = AppSettings()
    url = f"http://{app_settings.API_HOST}:{app_settings.API_PORT}/api/v1/food/campus/erica"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = await response.json()
            return response_json["restaurantList"]


@food_restaurant_router.post("")
async def campus(user_input: KakaoRequest) -> ServerResponse:
    restaurant_name = parse_user_utterance(user_input)
    menu_dict = None
    for menu_item in await fetch_menu_list_by_campus():
        if menu_item["name"] == restaurant_name:
            menu_dict = menu_item["menuList"]
    card_list: list[TextCard] = []

    if menu_dict is not None:
        description = ""
        for restaurant_key, menu_list in menu_dict.items():
            title = f"{restaurant_name}({restaurant_key})"
            for menu_item in menu_list:
                description += f"{menu_item['menu']}\n"
                description += f"가격 - {menu_item['price']}\n"
            card_list.append(TextCard(
                title=title, description=description.strip(), buttons=[]
            ))
    else:
        card_list = [
            TextCard(title=restaurant_name, description="제공되는 메뉴가 없습니다.", buttons=[]),
        ]

    return create_carousel_response(card_list, [])