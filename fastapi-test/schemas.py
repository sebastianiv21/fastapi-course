from pydantic import BaseModel

"""
ItemBase contains the fields that are common to both the create and update models.
"""


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


"""
Item is the Pydantic model that will be used in most of your app.
It contains all the fields that you want to return from your API.
"""


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str  # equivalent to Column(String) in models


"""
UserCreate has a password field that is not in UserBase to ensure that it is
not returned in the response from the API.
"""


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True


"""
Without orm_mode, if you returned a SQLAlchemy model from your path operation, 
it wouldn't include the relationship data.

Even if you declared those relationships in your Pydantic models.

But with ORM mode, as Pydantic itself will try to access the data it needs from 
attributes (instead of assuming a dict), you can declare the specific data you 
want to return and it will be able to go and get it, even from ORMs.
"""
