from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

"""
When accessing the attribute items in a User, as in my_user.items, 
it will have a list of Item SQLAlchemy models (from the items table) 
that have a foreign key pointing to this record in the users table.

When you access my_user.items, SQLAlchemy will actually go and fetch 
the items from the database in the items table and populate them here.

And when accessing the attribute owner in an Item, it will contain a User 
SQLAlchemy model from the users table. It will use the owner_id attribute/column 
with its foreign key to know which record to get from the users table.
"""


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
