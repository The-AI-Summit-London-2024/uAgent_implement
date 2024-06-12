from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from uagents import Model
from uagents.query import query
from router import main

import json,uvicorn

class TestRequest(Model):
    message: str
    
AGENT_ADDRESS="agent1qt6ehs6kqdgtrsduuzslqnrzwkrcn3z0cfvwsdj22s27kvatrxu8sy3vag0"

app = FastAPI()
router = APIRouter()

@app.get("/")
def read_root():
    agent_query()
    return {"Hello": "World"}

async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15.0)
    data = json.loads(response.decode_payload())
    return data["text"]

@app.post("/endpoint")
async def make_agent_call(req: TestRequest):
    try:
        res = await agent_query(req)
        return f"successful call - agent response: {res}"
    except Exception:
        return "unsuccessful agent call"
    
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main.router)

if __name__ == "__main__":
    config = uvicorn.Config("api_service:app", host='0.0.0.0', port=5000, log_level="info")
    server = uvicorn.Server(config)
    server.run()

