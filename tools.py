from langchain.tools import tool
from dotenv import load_dotenv
import os
import json
import requests
from tavily import TavilyClient
load_dotenv()






#weather tool

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
    
    response = requests.get(url)
    result = response.json()
    
    if str(result.get("cod")) != "200":
        return f"Error: {result.get('message', 'Could not fetch weather')}"
    
    temp = result["main"]["temp"]
    desc = result["weather"][0]["description"]
    
    return f"Weather in {city}: {desc}, {temp}°C"


# details tool


tavily = TavilyClient()

@tool
def city_details(city:str) ->str:
    """give details and about the city """

    response = tavily.search(
        query=f"Give useful information about {city}: famous places, attractions, culture, food, history and things to do",
        search_depth="advanced",
        max_results=3
    )


    return json.dumps(response, indent=2)


