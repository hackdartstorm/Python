"""
FastAPI Book Library Management API

A complete REST API for managing a book library.
Supports CRUD operations: Create, Read, Update, Delete.

Run with: uvicorn main:app --reload
Docs: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Book Library API",
    description="A simple API to manage a book library with CRUD operations",
    version="1.0.0",
)


# Pydantic models for request/response validation
class BookCreate(BaseModel):
    """Schema for creating a new book"""

    title: str = Field(..., min_length=1, description="Book title")
    author: str = Field(..., min_length=1, description="Author of the book")
    year: int = Field(..., description="Publication year")


class BookUpdate(BaseModel):
    """Schema for updating an existing book"""

    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)
    year: Optional[int] = Field(None, ge=1000, le=9999)


class Book(BaseModel):
    """Schema for book response"""

    book_id: int
    title: str
    author: str
    year: int


# In-memory data storage (replace with database in production)
books_db: list[Book] = [
    Book(book_id=1, title="Satanás", author="Mario Mendoza", year=2002),
    Book(book_id=2, title="Satanás", author="Mario Mendoza", year=2002),
    Book(book_id=3, title="Satanás", author="Mario Mendoza", year=2002),
]

# Auto-increment ID counter
next_book_id = 4


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Welcome to Book Library API",
        "docs": "/docs",
        "endpoints": {"books": "/books"},
    }


@app.get("/books", response_model=list[Book], tags=["Books"])
async def list_books():
    """Get all books"""
    return books_db


@app.get("/books/{book_id}", response_model=Book, tags=["Books"])
async def get_book(book_id: int):
    """Get a specific book by ID"""
    for book in books_db:
        if book.book_id == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found",
    )


@app.post(
    "/books", response_model=Book, status_code=status.HTTP_201_CREATED, tags=["Books"]
)
async def create_book(book_data: BookCreate):
    """Create a new book"""
    global next_book_id

    new_book = Book(
        book_id=next_book_id,
        title=book_data.title,
        author=book_data.author,
        year=book_data.year,
    )
    books_db.append(new_book)
    next_book_id += 1

    return new_book


@app.put("/books/{book_id}", response_model=Book, tags=["Books"])
async def update_book(book_id: int, book_update: BookUpdate):
    """Update an existing book"""
    for book in books_db:
        if book.book_id == book_id:
            if book_update.title is not None:
                book.title = book_update.title
            if book_update.author is not None:
                book.author = book_update.author
            if book_update.year is not None:
                book.year = book_update.year
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found",
    )


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Books"])
async def delete_book(book_id: int):
    """Delete a book"""
    for book_index, book in enumerate(books_db):
        if book.book_id == book_id:
            books_db.pop(book_index)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found",
    )
