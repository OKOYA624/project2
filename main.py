# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory database
books = []
next_id = 1

class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    publication_year: int
    genre: str

@app.post("/books/", response_model=Book)
def create_book(book: Book):
    global next_id
    book.id = next_id
    books.append(book.dict())
    next_id += 1
    return book

@app.get("/books/", response_model=List[Book])
def get_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for book in books:
        if book["id"] == book_id:
            book.update(updated_book.dict(exclude_unset=True))
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

