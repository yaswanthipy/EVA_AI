import os
import time


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from interview import router as interview_router
from evaluator import evaluate_answer as evaluate_answer_logic
from agora import send_agora_instruction, start_agora_agent, stop_agora_agent
from agora_token_builder import RtcTokenBuilder

app = FastAPI(
    title="EVA API",
    description="Enhanced Voice-based AI Interviewer",
    version="1.0.0"
)
app.include_router(
    interview_router,
    prefix="/interview",
    tags=["Interview"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnswerRequest(BaseModel):
    question_id: int
    question: str
    answer: str


class AgoraStartRequest(BaseModel):
    channel_name: str

class AgoraTokenRequest(BaseModel):
    channel_name: str
    uid: int = 2000

@app.post("/evaluate")
def evaluate_answer(data: AnswerRequest):

    result = evaluate_answer_logic(data.answer)

    return {
        "question_id": data.question_id,
        "question": data.question,
        "answer": data.answer,
        "score": result["score"],
        "feedback": result["feedback"]
    }
@app.post("/agora/start")
def start_agora(data: AgoraStartRequest):
    app_id = os.getenv("AGORA_APP_ID")
    app_certificate = os.getenv("AGORA_APP_CERTIFICATE")

    if not app_id:
        raise ValueError("AGORA_APP_ID is missing")

    if not app_certificate:
        raise ValueError("AGORA_APP_CERTIFICATE is missing")

    agent_uid = 1000

    expiration_time_in_seconds = 3600
    current_timestamp = int(time.time())
    privilege_expired_ts = (
        current_timestamp + expiration_time_in_seconds
    )

    agent_token = RtcTokenBuilder.buildTokenWithUid(
        app_id,
        app_certificate,
        data.channel_name,
        agent_uid,
        1,
        privilege_expired_ts
    )

    result = start_agora_agent(
        data.channel_name,
        agent_token
    )

    return {
        "status": "success",
        "channel_name": data.channel_name,
        "agora": result
    }

@app.post("/agora/stop/{agent_id}")
def stop_agora_agent_endpoint(agent_id: str):
    result = stop_agora_agent(agent_id)

    return {
        "status": "success",
        "agent_id": agent_id,
        "agora": result
    }

class AgoraThinkRequest(BaseModel):
    agent_id: str
    instruction: str


@app.post("/agora/think")
def agora_think(data: AgoraThinkRequest):
    result = send_agora_instruction(
        data.agent_id,
        data.instruction
    )

    return {
        "status": "success",
        "agent_id": data.agent_id,
        "agora": result
    }

@app.post("/agora/token")
def generate_agora_token(data: AgoraTokenRequest):

    app_id = os.getenv("AGORA_APP_ID")
    app_certificate = os.getenv("AGORA_APP_CERTIFICATE")

    if not app_id:
        raise ValueError("AGORA_APP_ID is missing")

    if not app_certificate:
        raise ValueError("AGORA_APP_CERTIFICATE is missing")

    expiration_time_in_seconds = 3600
    current_timestamp = int(time.time())
    privilege_expired_ts = current_timestamp + expiration_time_in_seconds

    token = RtcTokenBuilder.buildTokenWithUid(
        app_id,
        app_certificate,
        data.channel_name,
        data.uid,
        1,
        privilege_expired_ts
    )

    return {
        "token": token,
        "app_id": app_id,
        "channel_name": data.channel_name,
        "uid": data.uid
    }



@app.get("/")
def root():
    return {
        "message": "EVA API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "EVA backend"
    }