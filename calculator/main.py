from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Book_request(BaseModel):
    title: str
    author: str
    isbn: str
    published_date: str

class Book_response(BaseModel):
    book_id: int
    title: str
    author: str
    isbn: str
    published_date: str

books_db = {}  # In-memory database

@app.get("/books", response_model=list[Book_response])
def get_books():
    return [Book_response(book_id=id, **book.model_dump()) for id, book in books_db.items()]

@app.get("/books/{book_id}", response_model=Book_response)
def get_book(book_id: int):
    if book_id in books_db:
        book = books_db[book_id]
        return Book_response(book_id=book_id, **book.model_dump())
    raise HTTPException(status_code=404, detail="Book with the given ID is not present")

@app.post("/books/{book_id}", response_model=Book_response)
def post_book(book_id: int, book: Book_request):
    if book_id in books_db:
        raise HTTPException(status_code=409, detail="Book already present in the database")
    books_db[book_id] = book
    return Book_response(book_id=book_id, **book.model_dump())

@app.delete("/books/{book_id}", response_model=Book_response)
def del_book(book_id: int):
    if book_id in books_db:
        deleted_book = books_db.pop(book_id)
        return Book_response(book_id=book_id, **deleted_book.model_dump())
    raise HTTPException(status_code=404, detail="Book with the given ID is not present")
