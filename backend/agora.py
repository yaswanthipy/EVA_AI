import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()


AGORA_APP_ID = os.getenv("AGORA_APP_ID")
AGORA_CUSTOMER_ID = os.getenv("AGORA_CUSTOMER_ID")
AGORA_CUSTOMER_SECRET = os.getenv("AGORA_CUSTOMER_SECRET")
AGORA_PIPELINE_ID = os.getenv("AGORA_PIPELINE_ID")


def start_agora_agent(channel_name: str, agent_token: str):

    if not AGORA_APP_ID:
        raise ValueError("AGORA_APP_ID is missing")

    if not AGORA_CUSTOMER_ID:
        raise ValueError("AGORA_CUSTOMER_ID is missing")

    if not AGORA_CUSTOMER_SECRET:
        raise ValueError("AGORA_CUSTOMER_SECRET is missing")

    if not AGORA_PIPELINE_ID:
        raise ValueError("AGORA_PIPELINE_ID is missing")

    credentials = f"{AGORA_CUSTOMER_ID}:{AGORA_CUSTOMER_SECRET}"

    encoded_credentials = base64.b64encode(
        credentials.encode("utf-8")
    ).decode("utf-8")

    url = (
        "https://api.agora.io/api/conversational-ai-agent/v2/"
        f"projects/{AGORA_APP_ID}/join"
    )

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json",
    }

    payload = {
        "name": f"eva-interviewer-{channel_name}",
        "properties": {
            "channel": channel_name,
            "token": agent_token,
            "agent_rtc_uid": "1000",
            "remote_rtc_uids": ["2000"],
            "idle_timeout": 120,
        },
        "pipeline_id": AGORA_PIPELINE_ID,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(
            f"Agora API error {response.status_code}: {response.text}"
        )

    return response.json()


def stop_agora_agent(agent_id: str):
    if not AGORA_CUSTOMER_ID:
        raise ValueError("AGORA_CUSTOMER_ID is missing")

    if not AGORA_CUSTOMER_SECRET:
        raise ValueError("AGORA_CUSTOMER_SECRET is missing")

    credentials = f"{AGORA_CUSTOMER_ID}:{AGORA_CUSTOMER_SECRET}"

    encoded_credentials = base64.b64encode(
        credentials.encode("utf-8")
    ).decode("utf-8")

    url = (
    "https://api.agora.io/api/conversational-ai-agent/v2/"
    f"projects/{AGORA_APP_ID}/agents/{agent_id}/leave"
)

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        url,
        headers=headers,
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(
            f"Agora API error {response.status_code}: {response.text}"
        )

    return response.json()