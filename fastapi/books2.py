from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional

# Field is used for validation
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(title="id is not needed")
    # for pydanticv2, use:
    # id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    # gt = greater than, lt = less than
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=0)

    class Config:
        # for pydanticv2, use:
        # json_schema_extra = {}
        schema_extra = {
            "example": {
                "title": "HP1",
                "author": "Author 1",
                "description": "Book Description",
                "rating": 2,
                "published_date": 2000,
            }
        }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5, 2021),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5, 2023),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5, 2020),
    Book(4, "HP1", "Author 1", "Book Description", 2, 2001),
    Book(5, "HP2", "Author 2", "Book Description", 3, 1998),
    Book(6, "HP3", "Author 3", "Book Description", 1, 1900),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
# Path is used for validation, gt = greater than
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    # raise an exception if the book is not found
    raise HTTPException(status_code=404, detail="Book not found")


# get all books with a given rating value using query params
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(rating: int = Query(gt=0, lt=6)):
    return [book for book in BOOKS if book.rating == rating]


@app.get("/books/published/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Query(gt=0)):
    return [book for book in BOOKS if book.published_date == published_date]


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
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


@app.put("/books/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    # if the book is not changed, raise an exception
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")
