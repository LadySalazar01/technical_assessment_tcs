from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
import os
import jwt

API_KEY = os.getenv("API_KEY", "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c")
JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret_for_testing")


app = FastAPI()

class MessageIn(BaseModel):
    message: str
    to: str
    from_: str = Field(None, alias="from")
    timeToLifeSec: int

class MessageOut(BaseModel):
    message: str

def validate_api_key(key: str | None):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

def validate_jwt(token: str | None):
    if not token:
        raise HTTPException(status_code=401, detail="Missing JWT")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid JWT")

@app.post("/DevOps", response_model=MessageOut)
async def post_devops(body: MessageIn,
                      x_parse_rest_api_key: str | None = Header(None, alias="X-Parse-REST-API-Key"),
                      x_jwt_key: str | None = Header(None, alias="X-JWT-KWY")):
    validate_api_key(x_parse_rest_api_key)
    validate_jwt(x_jwt_key)
    pod_name = os.environ.get("HOSTNAME", "unknown-pod")
    return {"message": f"Hello {body.to} your message will be send"}
    # return {"message": f"Hello {body.to} your message will be send from pod {pod_name}"}


@app.get("/DevOps", response_class=PlainTextResponse)
@app.put("/DevOps", response_class=PlainTextResponse)
@app.delete("/DevOps", response_class=PlainTextResponse)
@app.patch("/DevOps", response_class=PlainTextResponse)
async def other_methods_devops():
    return PlainTextResponse("ERROR", status_code=405)

@app.get("/health")
async def health():
    return {"status": "ok"}
