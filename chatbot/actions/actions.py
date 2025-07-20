from datetime import datetime
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionTellTime(Action):
    def name(self) -> str:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        dispatcher.utter_message(text=f"The current time is {current_time}")
        return []
