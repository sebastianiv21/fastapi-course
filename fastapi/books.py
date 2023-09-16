from fastapi import FastAPI, Body

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]

app = FastAPI()


# create endpoints
@app.get("/books")
async def read_all_books():
    return BOOKS


# dynamic parameters
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book


# query parameters
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# get all books from a specific author
@app.get("/books/get_by/")
async def read_books_by_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return


"""
ORDER MATTERS!!!
The next endpoint goes after the previous one, because it can consume the same
requirements, producing an error indicating, in this case, that the category is missing.
"""


# path and query parameters
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    """
    This endpoint will return all books by a specific author and read_category_by_query<br>
    The author is a path parameter and the category is a query parameter (optional)<br>
    Query parameters are used like this: /books/Author%20One/?category=science
    """
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return


# post method
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return new_book


# put method
@app.put("/book/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book
    return updated_book


# delete method
@app.delete("/book/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
    return {"message": "Book deleted successfully"}
