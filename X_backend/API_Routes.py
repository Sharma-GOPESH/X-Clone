
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
from fastapi.middleware.cors import CORSMiddleware
from Routes import post_routes , user_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],  # Vite ka default port (CRA me 3000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post_routes.router)
app.include_router(user_routes.router)
