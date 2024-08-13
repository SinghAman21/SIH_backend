from pydantic import BaseModel,UUID4


class Users(BaseModel):
    first_Name:str
    last_Name:str
    role:str
    id:UUID4