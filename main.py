#Python imports
from uuid       import UUID
from datetime   import date
from typing     import Optional
#Pydantic imports
from pydantic import Field as FD
from pydantic import BaseModel as BMW
from pydantic import EmailStr
 

#FastAPI imports
from fastapi import FastAPI

#This is the app
app = FastAPI()

#This are the models to use
class UserBase(BMW):
    
    user_id : UUID = FD(
        ...,
    )

    email: EmailStr = FD(
        ...,
        example="micorreo@correo.com"
    )

class UserLogin(UserBase):

    password: str = FD(
        ...,
        min_length=8,
        max_length=22,
        example="perejil0000**"    
    )

class User(UserBase):

    first_name : str = FD(
        ...,
        min_length=1,
        max_length=20,
        example="Deyerli",
    )

    last_name : str = FD(
        ...,
        min_length=1,
        max_length=20,
        example="Cooper",
    )

    birth_date: Optional[date] = FD(default=None)



class Tweets(BMW):
    pass



@app.get(
    path="/"
    )
def home():
    return {"Twitter API" : "All the proccess are working" }