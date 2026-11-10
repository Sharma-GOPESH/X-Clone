
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

conn = psycopg2.connect(host="localhost" ,database="postgres",user="postgres" , password=12345678,cursor_factory=RealDictCursor)
cur =  conn.cursor() 

class Post_created(BaseModel):
   
    post_body: Annotated[str,Field(...,max_length=500,description="body of post")]

class Updated_post(BaseModel):
    post_body: Optional[str]
    posted_at : Optional[datetime]
    id:Optional[str]

def load_data():
    cur.execute("""SELECT * FROM post_data""")
    All_posts = cur.fetchall()
    conn.commit()
    return All_posts

router = APIRouter()

#endpoint to create a post
@router.post("/create_post")
def create_post(new_post : Post_created):
    
    
    cur.execute(SQL("""INSERT INTO post_data ({},{}) VALUES (%s,%s) """).format(Identifier("username"),
    Identifier("post_body")),(new_post.username,new_post.post_body))
    if cur.rowcount ==0:
        raise HTTPException(status_code=404,detail="post already exists!!")
    conn.commit()
    return JSONResponse(status_code=200,content="Post successfully created")

#endpoint to delete a post
@router.delete("/delete/{id}")
def delete_post(id:str):
    cur.execute(SQL("""DELETE FROM post_data WHERE {} = %s""").format(Identifier("id")),(id,))

    if cur.rowcount ==0:
        raise HTTPException(status_code=400,detail="Post does not exist")
    conn.commit()
    return JSONResponse(status_code=200,content="Post deleted successfully!!")


#endpoint to update a post
@router.put("/update_post")
def update_post(Updated_data : Updated_post):
    curr_time = datetime.now(timezone.utc)
    cur.execute(SQL("""SELECT posted_at FROM post_data WHERE {} = %s """).format(Identifier("id")),(Updated_data.id,)) 
    posted_time = cur.fetchone()
    posted = posted_time["posted_at"]
    conn.commit()
    if curr_time > posted + timedelta(minutes=10):
        raise HTTPException(status_code=404,detail="You can not update post!")
    
    
    cur.execute(SQL("""UPDATE post_data SET {} = %s WHERE {} = %s""").format(Identifier("post_body"),
    Identifier("id")),(Updated_data.post_body,Updated_data.id))

    if cur.rowcount ==0:
        raise HTTPException(status_code=400,detail="post does not exists")
    conn.commit()
    return JSONResponse(status_code=200,content="Post successfully Updated!!")
