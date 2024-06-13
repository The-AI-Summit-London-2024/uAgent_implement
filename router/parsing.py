from fastapi import HTTPException,APIRouter
from uagents import Model
from pydantic import BaseModel
from uagents.query import query

import base64,random,string,json,os

class APIRequest(BaseModel):
    file_data: str

class AgentRequest(Model):
    file_path: str
    
#AGENT_ADDRESS="agent1qt6ehs6kqdgtrsduuzslqnrzwkrcn3z0cfvwsdj22s27kvatrxu8sy3vag0"
AGENT_ADDRESS="agent1qwhr37xcn5gawtm5wdu7tqw8zypcxvf6y78p89su9cthysav3kjj7ud9823" # parsing_agent
QNA_AGNET = "agent1qtvx4ljdhk9rz3vep0pe56e7pzs884dtav0j56mfa3fz6lsx9u4hsdru0dc"


router = APIRouter(
    prefix="/parsing",
    tags=["parsing"],
)

def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def agent_query(file_name,destination):
    response = await query(destination=destination, message=AgentRequest(file_path=file_name), timeout=40.0)
    data = json.loads(response.decode_payload())
    return data["text"]


@router.post("/upload")
async def upload_file(request: APIRequest):
    try:
        file_data = base64.b64decode(request.file_data.split(",")[1])
        
        random_str = generate_random_string()

        if request.file_data.startswith("data:application/pdf;base64,"):
            file_name = f"file_{random_str}.pdf"
        elif request.file_data.startswith("data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,"):
            file_name = f"file_{random_str}.docx"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        file_path = os.path.join(os.path.dirname(__file__), '..', 'agents/files', file_name)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(file_data)
        
        try:
            res = await agent_query(os.path.join('files/',file_name),AGENT_ADDRESS)
        
            return {"response": res,"file_path":os.path.join('files/',file_name)}
        except Exception as e:
            return {"response": "unsuccessful agent call", "error": str(e)} 

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get_ten_q")
async def get_ten_q(request: AgentRequest):
    try:
        res = await agent_query(request.file_path, QNA_AGNET)
        return {"ten_q": res}
    except Exception as e:
        return {"response": "unsuccessful agent call", "error": str(e)} 

