import os
import requests

from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()


CITY_ALIAS = {
    "北京": "Beijing",
    "北京市": "Beijing",
    "上海": "Shanghai",
    "上海市": "Shanghai",
    "广州": "Guangzhou",
    "广州市": "Guangzhou",
    "深圳": "Shenzhen",
    "深圳市": "Shenzhen",
    "杭州": "Hangzhou",
    "杭州市": "Hangzhou",
    "南京": "Nanjing",
    "南京市": "Nanjing",
    "成都": "Chengdu",
    "成都市": "Chengdu",
    "重庆": "Chongqing",
    "重庆市": "Chongqing",
    "天津": "Tianjin",
    "天津市": "Tianjin",
    "西安": "Xi'an",
    "西安市": "Xi'an",
    "武汉": "Wuhan",
    "武汉市": "Wuhan",
    "东京": "Tokyo",
    "大阪": "Osaka",
}


@tool
def get_weather(
    city: str
) -> str:
    """
    查询城市天气。
    支持中文城市名到 OpenWeather 英文城市名的基础映射。
    """

    api_key = os.getenv(
        "OPENWEATHER_API_KEY"
    )

    if not api_key:
        return "天气查询失败: OPENWEATHER_API_KEY 未配置"

    query_city = CITY_ALIAS.get(
        city,
        city
    )

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": query_city,
        "appid": api_key,
        "units": "metric",
        "lang": "zh_cn"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

    except Exception as e:
        return f"天气查询失败: {str(e)}"

    print("\n========== WEATHER ==========\n")
    print(data)

    if "main" not in data:
        return (
            f"天气查询失败: "
            f"{data.get('message', data)}"
        )

    temp = data["main"]["temp"]

    desc = data["weather"][0]["description"]

    return (
        f"{city}天气："
        f"{desc}，"
        f"温度{temp}℃"
    )
