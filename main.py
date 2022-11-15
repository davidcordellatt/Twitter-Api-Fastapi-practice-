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
from fastapi import status, HTTPException
from fastapi import Body, Path, Form

#This is the app
app = FastAPI()

#Those are the models to use
class UserBase(BMW):
    
    user_id : UUID = FD(
        ...,
    )

    email: EmailStr = FD(
        ...,
        example=""
    )

class UserLogin(UserBase):

    password: str = FD(
        ...,
        min_length=8,
        max_length=22,
        example=""  ,  
    )

class User(UserBase):

    user_name: str = FD(
        ...,
        min_length=5,
        max_length=15,
        example="@cordellatt"
    )
    first_name : str = FD(
        ...,
        min_length=1,
        max_length=20,
        example="",
    )

    last_name : str = FD(
        ...,
        min_length=1,
        max_length=20,
        example="",
    )

    birth_date: Optional[date] = FD(default=None)

class UserRegister(User):

    password: str = FD(
        ...,
        min_length=8,
        max_length=22,
        example=""    
    )

class Tweet(BMW):
    
    tweet_id : str = FD(
        ...,
        min_length=5,
        max_length=15,
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

# Troll
@app.post(
    path="/F",
    tags=["Troll"]
    )
def troll():
    return "Me está llevando el diablo, send help"

#Home: Here you can see all tweets
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

#Login
@app.post(
    path="/login/{user_name}",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Login a user",
    tags=["User"],
)
def login(
            user_name: str = Path(..., title="User name"),
            password: str = Form(..., title="Password")
    ):
    """
    Login
    
    This Path Operation login the user in the app...

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
        result: list[dict] = json.load(user_data)

    user_position = 0

    while user_position < len(result) + 1:

        for user in result:

            if result[user_position]["user_name"] == user_name and result[user_position]["password"] == password:
                return user

            else:
                user_position = user_position + 1

            if user_position == len(result):
                raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail="That user don't exist!")

## Path Operations

### Users

#### Register a user
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

#### Show all user
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

#### Show a user:
@app.get(
    path="/user/{user_name}",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Show a User",
    tags=["User"],
)
def show_a_user(user_name: str = Path(..., title="User name")):
    """
    Show a user

    In this page you can see a user with her user name

    Parameters:
    - User's user name
    
    Returns a Json whith the basics users information:

    - user id : UUID
    - email : Emailstr
    - user name: str
    - first name: str
    - last name: str
    - birth date: datetime
    """
    with open("user.json", "r", encoding="utf-8") as user_data:
        result: list[dict] = json.load(user_data)

    user_position = 0

    while user_position < len(result) + 1:

        for user in result:

            if result[user_position]["user_name"] == user_name:
               return user
            
            if not result[user_position]["user_name"] == user_name:
                user_position = user_position + 1
            
            if user_position == len(result):
                raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail="That user don't exist!")

#### Delete a user
@app.delete(
    path="/user/{user_name}/delete",
    response_model= str,
    status_code= status.HTTP_200_OK,
    summary="Delete a user",
    tags=["User"],
)
def delete_user(user_name: str = Path(..., title="User name")):
    """
    Delete a user

    In this page you can delete a user with her user name

    Parameters:
    - User's user name
    
    Returns a message with the result
    """
    with open("user.json", "r+", encoding="utf-8") as user_data:
        result: list[dict] = json.load(user_data)
    

        for user in result:

            if user["user_name"] == str(user_name):
                result.remove(user)

                with open("user.json", "w", encoding="utf-8") as user_data:
                    user_data.seek(0)
                    json.dump(result, user_data)
                return f"The user {user_name} was be eliminated"

            
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="This user don't exist!"
            )

#### Update a user
@app.put(
    path="/user/{user_name}/update/",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Update a user",
    tags=["User"],
)
def update_user( 

    user_name : str = Path(
    ...,
    title="User name",
    description="Please insert the user that you want update",
    ),

    user: UserRegister = Body(...),
):
    """

    Update a user

    In this page you can update a user with his user name
    
    Parameters:
        user name: str
        user: UserRegister
        -

    Returns the new tweet model
    """

    user_name = str(user_name)
    user_dict = user.dict()
    user_dict['user_id'] = str(user_dict['user_id'])
    user_dict['birth_date'] = str(user_dict['birth_date'])

    with open("user.json", "r+", encoding="utf-8") as user_data:

        result = json.loads(user_data.read())

        for user in result:

            if  user['user_name'] == user_name:
                result[result.index(user)] = user_dict

                with open("user.json", "w", encoding="utf-8") as user_data:
                    user_data.seek(0)

                    user_data.write(json.dumps(result))
                return user_dict
            
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ese usuario no existe")

### Tweets

#### Post a tweet
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

#### Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model= Tweet,
    status_code= status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"],
)
def show_a_tweet(tweet_id: str = Path(..., title="First name")):
    """
    Show a tweet

    In this page you can see a user with her first name

    Parameters:
    - User's first name
    
    Returns a Json whith the basics users information:

    - tweet:id : UUID
    - content : str
    - created : datetime
    - updated : Optional[datetime]
    - by: UserBase
    """
    with open("tweets.json", "r", encoding="utf-8") as tweets_data:
        result: list[dict] = json.load(tweets_data)

    tweets_position = 0

    while tweets_position < len(result) + 1:
        for tweets in result:
            if result[tweets_position]["tweet_id"] == tweet_id:
               return tweets

            if not result[tweets_position]["tweet_id"] == tweet_id:
                tweets_position = tweets_position + 1
            
            if tweets_position == len(result):
                raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail="That tweet don't exist!")

#### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model= str,
    status_code= status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"],
)
def delete_tweet(tweet_id : str = Path(..., title="Tweet Id")):
    """
    Delete a tweet

    In this page you can delete a tweet with his id
    
    Parameters:
        -

    Returns a message with the result.
    """
    with open("tweets.json", "r+", encoding="utf-8") as tweets_data:
        result: list[dict] = json.load(tweets_data)
    
        for tweet in result:

            if tweet["tweet_id"] == str(tweet_id):
                result.remove(tweet)

                with open("tweets.json", "w", encoding="utf-8") as tweets_data:
                    tweets_data.seek(0)
                    json.dump(result, tweets_data)
                    return f"The tweet {tweet_id} was be eliminated"

            
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="This tweet don't exist!"
            )

#### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model= Tweet,
    status_code= status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"],
)
def update_tweet(
        
        tweet_id : str = Path(
            ..., 
            title="Tweet Id"
            ),

        new_content: str = Form(
            ...,
            title="New tweet information")

):
    """
    Update a tweet

    In this page you can update a tweet content with his id
    
    Parameters:
        tweet id: str
        new_content: str
        -

    Returns the new tweet model
    """
    with open("tweets.json", "r+", encoding="utf-8") as tweets_data:
        result: list[dict] = json.load(tweets_data)

        for tweet in result:

            if tweet['tweet_id'] == str(tweet_id):
                tweet['content'] = new_content

                with open("tweets.json", "w", encoding="utf-8") as tweets_data: 
                    tweets_data.seek(0)
                    tweets_data.write(json.dumps(result))
                    return tweet
            
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ese tweet no existe")