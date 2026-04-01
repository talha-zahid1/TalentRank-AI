from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
import middlewares.creating_jwt as jwt
get_token=OAuth2PasswordBearer(tokenUrl="login")
def isprotected(token:str=Depends(get_token)):
    jwt.verify_token(token=token)
    return token
def rolechecker(req_role:str):
    def rolech(token:str=Depends(isprotected)):
        data=jwt.verify_token(token=token)
        role=data["role"]
        if role==req_role:
            return data
        raise HTTPException(status_code=403,detail="Forbidden")
    return rolech
