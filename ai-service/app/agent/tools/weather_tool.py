import os
import requests

from dotenv import load_dotenv

from langchain.tools import tool

load_dotenv()


@tool
def get_weather(
    city: str
) -> str:
    """
    查询城市天气
    """

    api_key = os.getenv(
        "OPENWEATHER_API_KEY"
    )

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
    )

    params = {

        "q": city,

        "appid": api_key,

        "units": "metric",

        "lang": "zh_cn"
    }


    response = requests.get(
                url,
                params=params,
                timeout=10
    )

    data = response.json()

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