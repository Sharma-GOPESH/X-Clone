from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timezone , timedelta
import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

Secret_key=os.getenv("Secret_key")
Algorithm=os.getenv("Algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

Hash = "$argon2id$v=19$m=65536,t=3,p=4$8WkU9w1w5+dmAuV/Jpr3QQ$BIfUd2cRAZ9cZ+hpOIQwio5ez5Yyam70dz/uyGUA5NQ" 
password_hash = PasswordHash.recommended()
def hash_password(password:str):
    
    hashed_password = password_hash.hash(password)
    return hashed_password

def dummy_password(dummmy_pass):
    dummmy_pass = "JaiHind"
    dummy_password_hash = PasswordHash.recommended()
    dummy_hashed_pass = dummy_password_hash.hash(dummmy_pass)
    return dummy_hashed_pass


def create_jwt_token(Data:dict):
    copy_data = dict(Data.copy())
    copy_data["exp"] = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(copy_data, Secret_key , algorithm=Algorithm)


def verify_token(token :str) -> str:
    try:
        payload = jwt.decode(token,Secret_key,algorithms=[Algorithm])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
