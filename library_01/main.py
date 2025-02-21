from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from db.database import DATABASE_URL
from datetime import date

# Create a SQLAlchemy engine to connect to the database
engine = create_engine(DATABASE_URL)

# Create a session maker to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Create a FastAPI application
app = FastAPI()

# Define the Book model
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)  # Ensures ISBN is unique
    published_date = Column(Date, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)  # Index added for performance

# Create the database tables
Base.metadata.create_all(bind=engine)

# Define the Pydantic request model for creating books
class BookRequest(BaseModel):
    title: str
    author: str
    isbn: str
    published_date: date

    class Config:
        from_attributes = True

# Define the Pydantic response model for returning book data
class BookResponse(BookRequest):
    id: int
    is_deleted: bool

    class Config:
        from_attributes = True

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoint to get all books (excluding soft-deleted ones)
@app.get("/books", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.is_deleted == False).all()
    return [BookResponse.model_validate(book) for book in books]

# API endpoint to get a book by ID
@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id, Book.is_deleted == False).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book with the given ID is not present")
    return BookResponse.model_validate(book)

# API endpoint to create a new book
@app.post("/books", response_model=BookResponse)
def post_book(book: BookRequest, db: Session = Depends(get_db)):
    # Check if ISBN already exists
    existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")

    new_book = Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return BookResponse.model_validate(new_book)

# API endpoint to update a book by ID (Restore if it was deleted)
@app.put("/books/{book_id}", response_model=BookResponse)
def put_book(book_id: int, book: BookRequest, db: Session = Depends(get_db)):
    existing_book = db.query(Book).filter(Book.id == book_id).first()

    if not existing_book:
        raise HTTPException(status_code=404, detail="Book with the given ID is not present")

    # Restore book if it was deleted
    update_data = book.model_dump()
    update_data["is_deleted"] = False

    db.query(Book).filter(Book.id == book_id).update(update_data)
    db.commit()

    updated_book = db.query(Book).filter(Book.id == book_id).first()
    return BookResponse.model_validate(updated_book)

# API endpoint to soft-delete a book by ID
@app.delete("/books/{book_id}", status_code=204)
def del_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id, Book.is_deleted == False).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book with the given ID is not present")

    db.query(Book).filter(Book.id == book_id).update({"is_deleted": True})
    db.commit()

# API endpoint to restore a soft-deleted book by ID
@app.patch("/books/{book_id}/restore", response_model=BookResponse)
def restore_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id, Book.is_deleted == True).first()
    if not book:
        raise HTTPException(status_code=404, detail="Deleted book not found")

    db.query(Book).filter(Book.id == book_id).update({"is_deleted": False})
    db.commit()

    restored_book = db.query(Book).filter(Book.id == book_id).first()
    return BookResponse.model_validate(restored_book)
