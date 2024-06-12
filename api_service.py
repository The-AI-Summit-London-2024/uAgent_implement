from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import subprocess


app = FastAPI()
router = APIRouter()

@app.get("/")
def read_root():
    return {"Hello": "World"}

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Determine the base directory for the project
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(base_dir)
    # Construct paths to the agent scripts
    start_agent_path = os.path.join(base_dir, "agents", "doc_parsing_agent.py")

    # Start the dietagent
    subprocess.Popen(["python", start_agent_path])

# app.include_router(user_router.router)
# app.include_router(features_router.router)

if __name__ == "__main__":
    config = uvicorn.Config("api_service:app", host='0.0.0.0', port=5000, log_level="info")
    server = uvicorn.Server(config)
    server.run()

