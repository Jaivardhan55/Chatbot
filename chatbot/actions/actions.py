import os
import re
import time
import requests
from datetime import datetime
from typing import Any, Dict, List, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv

load_dotenv()  

# ------------------ Utility Functions ------------------

def extract_numbers(text: str) -> List[float]:
    return list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", text)))

def determine_operation(text: str) -> Optional[str]:
    ops = {
        "add": ["plus", "+", "add"],
        "subtract": ["minus", "-", "subtract"],
        "multiply": ["multiply", "*", "times"],
        "divide": ["divide", "/"]
    }
    for op, keywords in ops.items():
        if any(k in text for k in keywords):
            return op
    return None

def calculate(a: float, b: float, operation: str) -> Optional[float]:
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return None
        return a / b
    return None

def get_weather_data(city: str) -> Optional[Dict[str, Any]]:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") == 200:
            return {
                "temp": data["main"]["temp"],
                "desc": data["weather"][0]["description"]
            }
    except Exception as e:
        print(f"Weather API error: {e}")
    return None

# ------------------ Action Classes ------------------

class ActionTellTime(Action):
    def name(self) -> str:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        now = datetime.now().strftime("%H:%M:%S")
        dispatcher.utter_message(text=f"The current time is {now}")
        return []


class ActionDoMath(Action):
    def name(self) -> str:
        return "action_do_math"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        user_msg = tracker.latest_message.get("text", "")
        numbers = extract_numbers(user_msg)

        if len(numbers) < 2:
            dispatcher.utter_message(text="Please give me at least two numbers to calculate.")
            return []

        operation = determine_operation(user_msg)
        if not operation:
            dispatcher.utter_message(text="I couldn't understand the operation.")
            return []

        result = calculate(numbers[0], numbers[1], operation)
        if result is None:
            dispatcher.utter_message(text="I can't divide by zero.")
            return []

        dispatcher.utter_message(text=f"The result is {result}")
        return []


class ActionGetWeather(Action):
    def name(self) -> str:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        location = tracker.get_slot("location")
        if not location:
            dispatcher.utter_message(text="Please tell me the city you'd like the weather for.")
            return []

        city = location.strip().title()
        weather = get_weather_data(city)

        if weather:
            dispatcher.utter_message(text=f"The weather in {city} is {weather['temp']}°C with {weather['desc']}.")
        else:
            dispatcher.utter_message(text=f"Couldn't find weather data for {city}.")
        return []
