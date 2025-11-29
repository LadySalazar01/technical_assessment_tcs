import time, uuid, jwt
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app, API_KEY, JWT_SECRET


client = TestClient(app)

def gen_jwt():
    payload = {
        "jti": str(uuid.uuid4()), 
        "iat": int(time.time()), 
        "exp": int(time.time())+60
        }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def test_post_success():
    token = gen_jwt()
    resp = client.post("/DevOps",
                       headers={
                           "X-Parse-REST-API-Key": API_KEY,
                           "X-JWT-KWY": token
                       },
                       json={"message":"This is a test","to":"Juan Perez","from":"Rita Asturia","timeToLifeSec":45})
    assert resp.status_code == 200
    assert resp.json() == {"message":"Hello Juan Perez your message will be send"}

def test_get_error():
    resp = client.get("/DevOps")
    assert resp.status_code == 405
    assert resp.text == "ERROR"

def test_put_error():
    resp = client.put("/DevOps")
    assert resp.status_code == 405
    assert resp.text == "ERROR"
