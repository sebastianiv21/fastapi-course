from fastapi import FastAPI
from typing import Optional

# Field is used for validation
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(title="id is not needed")
    # for pydanticv2, use:
    # id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    # gt = greater than, lt = less than
    rating: int = Field(gt=-1, lt=6)

    class Config:
        # for pydanticv2, use:
        # json_schema_extra = {}
        schema_extra = {
            "example": {
                "title": "HP1",
                "author": "Author 1",
                "description": "Book Description",
                "rating": 2,
            }
        }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5),
    Book(4, "HP1", "Author 1", "Book Description", 2),
    Book(5, "HP2", "Author 2", "Book Description", 3),
    Book(6, "HP3", "Author 3", "Book Description", 1),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    # convert the request to a Book object
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


"""
Book(**book_request.dict()) is the same as:
Book(id=book_request.id, title=book_request.title, author=book_request.author, 
    description=book_request.description, rating=book_request.rating)

The ** operator is used to unpack an iterable (list, tuple, dict, set, etc.) in Python.

for pydanticv2, use:
new_book = Book(**book_request.model_dump())
"""


def find_book_id(book: Book):
    # if (len(BOOKS)) > 0:
    #     # find the max id and add 1
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book
