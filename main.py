#Python imports
import json
from uuid       import UUID
from datetime   import date
from datetime   import datetime
from typing     import Optional, List


#Pydantic imports
from pydantic import Field as FD
from pydantic import BaseModel as BMW
from pydantic import EmailStr
 
#FastAPI imports
from fastapi import FastAPI
from fastapi import status
from fastapi import Body

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

class UserRegister(User):

    password: str = FD(
        ...,
        min_length=8,
        max_length=22,
        example="perejil0000**"    
    )
class Tweets(BMW):
    
    tweet_id : UUID = FD(
        ...,
    )

    content: str = FD(
        ...,
        min_length=1,
        max_length=256,
        example="Hello dear. This is the first tweet from my Api"
    )

    created_at: date = FD(default=datetime.now())
    update_at: Optional[date] = FD(default=None)

    by : User = FD(
        ...,
    )

#Path Operactions

## Troll
@app.post(
    path="/F",
    tags=["Troll"]
    )
def troll():
    return "Me está llevando el diablo, send help"

## Users
@app.post(
    path="/signup",
    response_model= User,
    status_code= status.HTTP_201_CREATED,
    summary="Register a new User",
    tags=["User"],
)
def signup(user: UserRegister = Body(...)):
    """
    Sign-Up

    Register a user in the app
    
    Parameters:
        - Request body parameter
            - user: UserRegister
    
    Returns a Json whith the basice user information:

        - user id : UUID
        - email : Emailstr
        - first name: str
        - last name: str
        - birth date: datetime
    """
    with open("user.json", "r+", encoding="utf-8") as user_data:
        results = json.loads(user_data.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        user_data.seek(0)
        user_data.write(json.dumps(results))
        return user

@app.post(
    path="/login",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Login a user",
    tags=["User"],
)
def login():
    """
    Login

    Login a user in the app
    
    Parameters:
        - Request body parameter
            - user: UserRegister
    
    Returns a Json whith the basice user information:

        - user id : UUID
        - email : Emailstr
        - first name: str
        - last name: str
        - birth date: str 
    """

@app.get(
    path="/users",
    response_model= List[User],
    status_code= status.HTTP_200_OK,
    summary="Show all the users",
    tags=["User"],
)
def show_all_users():
    """
    Show all users

    In this page you can see all the users in the app
    
    Parameters:
        - Request body parameter:
        - user: UserRegister
    
    Returns a Json whith the basics users information:

        - user id : UUID
        - email : Emailstr
        - first name: str
        - last name: str
        - birth date: datetime
    """
    with open("user.json", "r", encoding="utf-8") as user_data:
        results = json.loads(user_data.read())
        return results

@app.get(
    path="/users/{user_id}",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Show a User",
    tags=["User"],
)
def show_a_user():
    pass

@app.delete(
    path="/user/{user_id}/delete",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Delete a user",
    tags=["User"],
)
def delete_user():
    pass

@app.put(
    path="/user/{user_id}/update",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Update a user",
    tags=["User"],
)
def update_user():
    pass

## Home
@app.get(
    path="/",
    response_model= List[Tweets],
    status_code= status.HTTP_200_OK,
    summary="Show all the tweets",
    tags=["Tweets"],
)
def home():
    return {"Twitter API" : "All the proccess are working" }

## Tweets
@app.get(
    path="/post",
    response_model= Tweets,
    status_code= status.HTTP_201_CREATED,
    summary="Created a new tweet",
    tags=["Tweets"],
)
def signup():
    pass

@app.get(
    path="/tweets/{tweet_id}",
    response_model= Tweets,
    status_code= status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"],
)
def show_a_tweet():
    pass

@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model= Tweets,
    status_code= status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"],
)
def delete_tweet():
    pass

@app.put(
    path="/tweets/{tweet_id}/update",
    response_model= Tweets,
    status_code= status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"],
)
def update_tweet():
    pass
