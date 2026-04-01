from datetime import datetime,timedelta
from fastapi import HTTPException
from jose import jwt,JWTError,ExpiredSignatureError
secret_key="Mysecret"
Algorithm="HS256"
exp_time=60
def create_token(email:str,role:str):
    
    payload={
        "sub":email,
        "role":role,
        "exp":datetime.utcnow()+timedelta(minutes=exp_time)
    }
    token=jwt.encode(payload,secret_key,Algorithm)
    return token
def verify_token(token:str):
    try:
        payload=jwt.decode(token=token,key=secret_key,algorithms=[Algorithm])
        return {"email":payload.get("sub"),"role":payload.get("role")}
    except ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="Expire token")
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")