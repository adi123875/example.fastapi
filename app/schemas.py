from pydantic import BaseModel,EmailStr,conint
from datetime import datetime 
from typing import Optional
class postBase(BaseModel):
    title:str
    content:str
    published:bool=True


class postcreate(postBase):
    pass

class userout(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class config:
        orm_mode=True

        
class post(postBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:userout
    class config:
        orm_mode=True

class postout(BaseModel):
    post:post
    votes:int
    class config:
        orm_mode=True
    
    

class usercreate(BaseModel):
    email:EmailStr
    password:str
    



class userLogin(BaseModel):
    email:EmailStr
    password:str


class token(BaseModel):
    access_token:str
    token_type:str

class tokendata(BaseModel):
    id:Optional[int]=None


class vote(BaseModel):
    post_id:int
    dir:conint(le=1) # type: ignore