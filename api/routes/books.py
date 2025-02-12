from typing import OrderedDict
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from api.db.schemas import Book, Genre

# InMemoryDB class with the required methods
class InMemoryDB:
    books: dict[int, Book]

    def __init__(self):
        self.books = {
            1: Book(
                id=1,
                title="The Hobbit",
                author="J.R.R. Tolkien",
                publication_year=1937,
                genre=Genre.SCI_FI,
            ),
            2: Book(
                id=2,
                title="The Lord of the Rings",
                author="J.R.R. Tolkien",
                publication_year=1954,
                genre=Genre.FANTASY,
            ),
            3: Book(
                id=3,
                title="The Return of the King",
                author="J.R.R. Tolkien",
                publication_year=1955,
                genre=Genre.FANTASY,
            ),
        }

    def get_books(self) -> OrderedDict[int, Book]:
        return OrderedDict(self.books)

    def add_book(self, book: Book) -> None:
        self.books[book.id] = book

    def update_book(self, book_id: int, book: Book) -> Book:
        if book_id in self.books:
            self.books[book_id] = book
            return book
        raise ValueError("Book not found")

    def delete_book(self, book_id: int) -> None:
        if book_id in self.books:
            del self.books[book_id]
        else:
            raise ValueError("Book not found")

    def get_book_by_id(self, book_id: int) -> Book | None:
        return self.books.get(book_id)


# Initialize InMemoryDB instance
db = InMemoryDB()

# FastAPI Router for the Books routes
router = APIRouter()

# Create a new book
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    db.add_book(book)
    return book  # FastAPI will automatically return JSON

# Get all books
@router.get(
    "/", response_model=OrderedDict[int, Book], status_code=status.HTTP_200_OK
)
async def get_books() -> OrderedDict[int, Book]:
    return db.get_books()

# Get a single book by its ID
@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int):
    book = db.get_book_by_id(book_id)
    if book:
        return book  # Return book directly, FastAPI converts it to JSON
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

# Update an existing book
@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: Book) -> Book:
    existing_book = db.get_book_by_id(book_id)
    if not existing_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    updated_book = db.update_book(book_id, book)
    return updated_book  # Return updated book directly

# Delete a book
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int) -> None:
    book = db.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete_book(book_id)
    return None  # No content returned on successful deletion