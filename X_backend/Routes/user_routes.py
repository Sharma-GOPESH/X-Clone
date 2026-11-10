
from pydantic import BaseModel,Field , field_validator, model_validator,computed_field ,  EmailStr 
from typing import List , Dict , Optional , Annotated , Literal
from fastapi import FastAPI , Path,HTTPException,Query , APIRouter
from fastapi.responses import JSONResponse
import json
from datetime import datetime, timezone , timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL , Identifier
from utils import *
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from Routes import post_routes , user_routes

#connecting the data base to the server
conn = psycopg2.connect(host="localhost" ,database="postgres",user="postgres" , password=12345678,cursor_factory=RealDictCursor)
cur =  conn.cursor()

    
class user(BaseModel):
    email: Annotated[EmailStr,Field(...,description="email id of the user")]
    password : Annotated[str,Field(...,min_length=8,description="the password of the user account")]
    username: Annotated[str,Field(...,min_length=6,max_length=15,description="Username of User")]
   
class userout(BaseModel):
    user_id : Annotated[str,Field(...,description="id of user")]
    email: Annotated[EmailStr,Field(...,description="email id of the user")]
    created_at : Annotated[datetime,Field(...,description="User joined date and time")]

class Delete_User(BaseModel):
    password : Annotated[str,Field(...,min_length=8,description="the password of the user account")]
    email: Annotated[EmailStr,Field(...,description="email id of the user")]

class User_Profile(BaseModel):
    username: Annotated[str,Field(description="Username of User")]
    created_at : Annotated[datetime,Field(description="User joined date and time")]
    total_post : Annotated[list,Field(description="total posts of user")]
    follower_count :Annotated[int,Field(description="Total followers of the user")]
    following_count: Annotated[int,Field(description="Total following of the user")]
    is_following:Annotated[bool,Field(description="does you follow this user")]
    user_id : Annotated[str,Field(description="id of user")]

def load_user_profile_data():
    cur.execute("""SELECT * FROM user_profile_data""")
    All_users_profile_data = cur.fetchall()
    conn.commit()
    return All_users_profile_data



router = APIRouter()
#endpoint to register new user
@router.post("/users")
def Add_user(new_user : user):
    new_password = hash_password(new_user.password)
    cur.execute(""" SELECT * FROM user_data WHERE email_id = (%s)""",(new_user.email,))
    if cur.rowcount == 0:
     cur.execute("""SELECT username FROM user_data WHERE username = (%s)""",(new_user.username,))
     if cur.rowcount != 0:
         raise HTTPException(status_code=404,detail="This username already Exists")
     
     cur.execute(SQL("""INSERT INTO user_data ({},{},{}) VALUES (%s,%s,%s)""").format(Identifier("username"),
     Identifier("password"),
     Identifier("email_id")),
     (new_user.username,new_password,new_user.email))
     conn.commit()
     cur.execute("""SELECT created_at FROM user_data WHERE email_id = (%s)""",(new_user.email,))
     created_at = cur.fetchone()["created_at"]
     if created_at is None:
         raise HTTPException(status_code=404,detail="user does not exists!!")
     
     cur.execute("""INSERT INTO user_profile_data (username,created_at) VALUES (%s,%s)""",(new_user.username,created_at))
     conn.commit()
     token = create_jwt_token({"sub":new_user.username})
     return token

    raise HTTPException(status_code=404,detail="user already exists")

#endoint to login an user
@router.post("/user_login")
def user_login(login_details : Delete_User):
    cur.execute("""SELECT password FROM user_data WHERE email_id = (%s)""",(login_details.email,))
    hash_pass = cur.fetchone()
    if hash_pass is None:
        password_hash.verify(login_details.password,Hash)
        raise HTTPException(status_code=401, detail="invalid credentials")
    
    stored_hash = hash_pass["password"]
    if not password_hash.verify(login_details.password,stored_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")
    
    cur.execute("""SELECT username FROM user_data WHERE email_id = (%s) """,(login_details.email,))
    user_name = cur.fetchone()
    login_token = create_jwt_token({"sub":user_name})
    return login_token
     
@router.delete("/delete")
def delete_user(delete_user : Delete_User):
    cur.execute("""SELECT username FROM user_data WHERE email_id = (%s)""",(delete_user.email,))
    username_of_deleting_user = cur.fetchone()["username"]
    conn.commit()
    cur.execute("""SELECT password FROM user_data WHERE email_id = (%s)""",(delete_user.email,))
    hash_pass = cur.fetchone()
    if hash_pass == None:
            password_hash.verify(delete_user.password,Hash)
            raise HTTPException(status_code=401, detail="invalid credentials")
    stored_hash = hash_pass["password"]

    if hash_pass == None:
        password_hash.verify(delete_user.password,Hash)
        raise HTTPException(status_code=401, detail="invalid credentials")

    if not password_hash.verify(delete_user.password,stored_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")

    cur.execute("""DELETE FROM user_data WHERE email_id = (%s) RETURNING email_id , created_at """,(delete_user.email,))
    deleted_user = cur.fetchone()
    cur.execute("""DELETE FROM post_data WHERE username = (%s)""",(username_of_deleting_user,))
    if deleted_user == None:
        raise HTTPException(status_code=404,detail="this user does  not exists")
    conn.commit()
    return deleted_user

#endpoint to view an user's profile
@router.get("/user_profile")
def getting_user_profile(username : str):
    cur.execute("""SELECT * FROM user_profile_data WHERE username = (%s)""",(username,))
    users = cur.fetchone()

    if users is None:
        raise HTTPException(status_code=404,detail="User does not exists")

    return users


