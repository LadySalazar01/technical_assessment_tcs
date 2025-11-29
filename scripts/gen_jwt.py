#!/usr/bin/env python3
import jwt, time, uuid, os

JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret_for_testing")
payload = {
    "jti": str(uuid.uuid4()),
    "iat": int(time.time()),
    "nbf": int(time.time()),
    "exp": int(time.time()) + 600
}
token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
print(token)
