from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import os


class PushNotificationInput(BaseModel):
    """A message to be sent to the user."""
    message: str = Field(..., description="The message for the push notification.")

class PushNotificationTool(BaseTool):
    name: str = "Send a push notification"
    description: str = (
        "This tool is used to send push notification to the user."
    )
    args_schema: Type[BaseModel] = PushNotificationInput

    def _run(self, message: str) -> str:
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        pushover_url= "https://api.pushover.net/1/messages.json"

        print(f"Push: {message}")
        payload = {
            "token": pushover_token,
            "user": pushover_user,
            "message": message
        }
        requests.post(pushover_url, data=payload)
        return "Push notification sent successfully."
