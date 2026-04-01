from passlib.context import CryptContext
pwd_ctxt=CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash_pwd(password:str):
    return pwd_ctxt.hash(password)
def verify_password(plain_pass,hashed_pass):
    return pwd_ctxt.verify(plain_pass,hashed_pass)