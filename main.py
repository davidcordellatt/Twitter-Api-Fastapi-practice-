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
        example="perejil0000**"  ,  
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

class Tweet(BMW):
    
    tweet_id : UUID = FD(
        ...,
    )

    content: str = FD(
        ...,
        min_length=1,
        max_length=256,
        example="Hello dear. This is the first tweet from my Api"
    )

    created_at: datetime = FD(default=datetime.now())
    updated_at: Optional[datetime] = FD(default=None)
    by: UserBase = FD (...)

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
    pass

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
#Path Operactions

## Tweets
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post_a_tweet(tweet : Tweet = Body(...)):
    """
    Post a Tweet

    In this page you can create a new tweet
    
    Parameters:
    - Request body parameter:
        - tweet: Tweets
    
    Returns a Json whith the basics users information:

    - tweet:id : UUID
    - content : str
    - created : datetime
    - updated : Optional[datetime]
    - by: UserBase
    """

    with open("tweets.json", "r+", encoding="utf-8") as tweet_data:
        results = json.loads(tweet_data.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        if tweet_dict["updated_at"] is not None:
            tweet_dict["updated_at"] = str(tweet_dict["updated_at"])

        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["email"] = str(tweet_dict["by"]["email"])        
        results.append(tweet_dict)
        tweet_data.seek(0)
        tweet_data.write(json.dumps(results))
        return tweet

@app.get(
    path="/tweets/{tweet_id}",
    response_model= Tweet,
    status_code= status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"],
)
def show_a_tweet():
    pass

@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model= Tweet,
    status_code= status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"],
)
def delete_tweet():
    pass

@app.put(
    path="/tweets/{tweet_id}/update",
    response_model= Tweet,
    status_code= status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"],
)
def update_tweet():
    pass

## Home
@app.get(
    path="/",
    response_model= List[Tweet],
    status_code= status.HTTP_200_OK,
    summary="Show all the tweets",
    tags=["Home"],
)
def home():
    """
    Show all tweets

    In this page you can see all the tweers in the app
    
    Parameters:
        -

    Returns a Json whith the basics users information:

    - tweet:id : UUID
    - content : str
    - created : datetime
    - updated : Optional[datetime]
    - by: UserBase
    """
    with open("tweets.json", "r", encoding="utf-8") as tweets_data:
        results = json.loads(tweets_data.read())
        return results