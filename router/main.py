from fastapi import HTTPException,APIRouter
from uagents import Model
from pydantic import BaseModel
from uagents.query import query

import base64,random,string,json,os

class FileRequest(BaseModel):
    file_data: str

class FilePathRequest(Model):
    file_path: str
    
#AGENT_ADDRESS="agent1qt6ehs6kqdgtrsduuzslqnrzwkrcn3z0cfvwsdj22s27kvatrxu8sy3vag0"
AGENT_ADDRESS="agent1qwhr37xcn5gawtm5wdu7tqw8zypcxvf6y78p89su9cthysav3kjj7ud9823" # parsing_agent

router = APIRouter(
    prefix="/main",
    tags=["main"],
)

def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def agent_query(file_name,destination):
    response = await query(destination=destination, message=FilePathRequest(file_path=file_name), timeout=15.0)
    data = json.loads(response.decode_payload())
    return data["text"]


@router.post("/upload")
async def upload_file(request: FileRequest):
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
        
        await agent_query(os.path.join('files/',file_name),AGENT_ADDRESS)

        return {"detail": f"File saved as {file_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
